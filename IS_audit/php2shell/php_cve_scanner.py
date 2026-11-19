#!/usr/bin/env python3
"""Неразрушающая сетевая оценка PHP2Shell (CVE-2026-109618/109619).

Версия: 1.1. Дата: 11.2026.
Методическая основа: php_cve_scanner.py из предоставленного архива
php2shell-for-IB-2026-10-23. Независимая реализация для службы ИБ.
Только обычные HTTP GET без тела, без аутентификации и редиректов.
Сетевой баннер — косвенное свидетельство; наличие патча не доказывается.
"""

import argparse
import csv
import ipaddress
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

# Пороговые версии обеих CVE, сверенные с CERT-EU 2026-018.
FIXED = {(8, 2): 35, (8, 3): 36, (8, 4): 27, (8, 5): 12}
CVES = ('CVE-2026-109618', 'CVE-2026-109619')
# Пары порт/протокол по умолчанию; FastCGI не опрашивается как HTTP.
DEFAULT_PORTS = (80, 443, 1443, 8000, 8080, 8081, 8443, 8888, 9443)
TLS_PORTS = (443, 1443, 8443, 9443)
DEFAULT_PATHS = ('/', '/index.php')
ZONES = ('corp', 'vds', 'mgmt')
MAX_PORTS = 16
MAX_PATHS = 8
MIN_DELAY = 0.3
VERSION = '1.1'
# Версия распознаётся только непосредственно после имени PHP.
PHP_VERSION = re.compile(
    r'\bPHP[/ ]+(\d+)\.(\d+)(?:\.(\d+))?'
    r'([^\s,;]*)', re.IGNORECASE
)
PHP_MARK = re.compile(r'\bPHP\b', re.IGNORECASE)
SESSION_MARK = re.compile(r'^\s*(PHPSESSID|PHP_SESSION_ID)=', re.I)
HOST_RE = re.compile(r'^[a-zA-Z0-9_.-]{1,253}$')
STATUS_LABELS = {
    'potentially_affected': 'Потенциально уязвим (по баннеру)',
    'fixed_banner': 'Баннер не ниже исправленной версии',
    'unknown_build': 'Требуется проверка сборки',
    'php_hint': 'Признак PHP, версия неизвестна',
    'not_detected': 'Признаки PHP не выявлены',
    'unavailable': 'Сетевой/HTTP-ответ не получен',
    'tcp_only': 'TCP доступен; протокол не определён',
}


class ArgumentParser(argparse.ArgumentParser):
    """Отделить ошибки CLI (1) от потенциальной уязвимости (2)."""

    def error(self, message):
        """Вывести сообщение об ошибке и завершить работу с кодом 1."""
        self.print_usage(sys.stderr)
        self.exit(1, f'{self.prog}: error: {message}\n')


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """Запретить переход на другой URL, включая другой хост."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        """Вернуть None, чтобы исходный 3xx был доступен как HTTPError."""
        return None


def validate_host(raw):
    """Вернуть IP/FQDN без схемы, порта, CIDR и учётных данных.

    Args:
        raw (str): Введённое пользователем имя или IP.
    Raises:
        ValueError: Строка не является разрешённым одиночным хостом.
    """
    host = raw.strip()
    try:
        return str(ipaddress.ip_address(host))
    except ValueError:
        if HOST_RE.fullmatch(host) and not host.startswith('-'):
            return host
        raise ValueError('Укажите один FQDN или IP без URL/CIDR.')


def parse_ports(raw):
    """Разобрать auto или отдельные TCP-порты через запятую.

    Args:
        raw (str): Пустая строка, auto либо список портов.
    Returns:
        list: Уникальные порты в исходном порядке.
    Raises:
        ValueError: Неверное значение или превышен лимит портов.
    """
    if raw.strip().lower() in ('', 'auto'):
        return list(DEFAULT_PORTS)
    ports = list(dict.fromkeys(int(p.strip()) for p in raw.split(',')))
    if len(ports) > MAX_PORTS or any(not 1 <= p <= 65535 for p in ports):
        raise ValueError('Допустимо до 16 портов в диапазоне 1–65535.')
    return ports


def validate_paths(paths):
    """Разрешить только заданные абсолютные пути на том же хосте.

    Args:
        paths (list): Пути без query, fragment и управляющих символов.
    Returns:
        list: Уникальные валидированные пути.
    Raises:
        ValueError: Путь выходит за пределы допустимого формата.
    """
    result = list(dict.fromkeys(paths))
    if not result or len(result) > MAX_PATHS:
        raise ValueError('Допустимо от 1 до 8 путей.')
    for path in result:
        parts = urlsplit(path)
        if (not path.startswith('/') or path.startswith('//')
                or parts.scheme or parts.netloc or parts.query
                or parts.fragment or '\\' in path or '%' in path
                or any(ord(c) < 33 or ord(c) > 126 for c in path)
                or len(path) > 200):
            raise ValueError('Недопустимый путь: ' + repr(path))
    return result


def classify_php(banner):
    """Оценить только заявленную версию PHP по таблице FIXED.

    Args:
        banner (str): Значение заголовка X-Powered-By.
    Returns:
        tuple: Код оценки, версия (или None), краткое обоснование.
    """
    match = PHP_VERSION.search(banner)
    if not match:
        if PHP_MARK.search(banner):
            return 'php_hint', None, 'PHP указан без полной версии.'
        return 'not_detected', None, 'Нет распознаваемого PHP-баннера.'
    major, minor, patch, suffix = match.groups()
    branch = (int(major), int(minor))
    version = f'{major}.{minor}'
    if patch is not None:
        version += '.' + patch
    version += suffix
    # Неполный номер, суффикс и неизвестная ветка не дают вердикт.
    if patch is None or suffix or branch not in FIXED:
        return 'unknown_build', version, 'Уточнить пакет и backport.'
    threshold = f'{major}.{minor}.{FIXED[branch]}'
    if int(patch) < FIXED[branch]:
        return 'potentially_affected', version, 'Ниже ' + threshold
    return 'fixed_banner', version, 'Не ниже ' + threshold


def resolve_host(host):
    """Получить уникальные IP из системного DNS.

    Args:
        host (str): Проверенный FQDN или IP.
    Returns:
        list: IP-адреса в строковом виде.
    Raises:
        OSError: Ошибка DNS или системного резолвера.
    """
    return sorted({row[4][0] for row in socket.getaddrinfo(
        host, None, type=socket.SOCK_STREAM
    )})


def tcp_check(host, port, timeout):
    """Проверить один TCP-порт.

    Args:
        host (str): Имя или IP объекта.
        port (int): Номер TCP-порта.
        timeout (float): Таймаут подключения в секундах.
    Returns:
        tuple: Доступность, IP соединения либо None, тип ошибки либо None.
    """
    try:
        with socket.create_connection((host, port), timeout) as conn:
            return True, conn.getpeername()[0], None
    except OSError as exc:
        return False, None, type(exc).__name__


def make_request(host, port, scheme, path, timeout, context):
    """Выполнить GET без тела и извлечь только диагностические признаки.

    HTTP 3xx/4xx/5xx сохраняются как ответы, а не как сетевые ошибки.
    Тело, Location, значения cookies и необработанные заголовки не пишутся.
    TLS проверяется переданным SSLContext; системный прокси отключён.
    Args:
        host (str): Имя или IP объекта.
        port (int): TCP-порт веб-сервиса.
        scheme (str): http либо https.
        path (str): Проверенный абсолютный путь.
        timeout (float): Таймаут сетевой операции.
        context (ssl.SSLContext): Режим доверия TLS.
    Returns:
        dict: Путь, HTTP-статус, версия PHP, категория, обоснование.
    """
    url_host = '[' + host + ']' if ':' in host else host
    url = f'{scheme}://{url_host}:{port}{path}'
    request = urllib.request.Request(
        url, headers={'User-Agent': 'php2shell-inventory/1.1'}, method='GET'
    )
    opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({}), NoRedirect(),
        urllib.request.HTTPSHandler(context=context)
    )
    try:
        response = opener.open(request, timeout=timeout)
    except urllib.error.HTTPError as exc:
        response = exc
    except (OSError, urllib.error.URLError) as exc:
        reason = getattr(exc, 'reason', exc)
        return {'path': path, 'http_status': None, 'php_version': None,
                'status': 'unavailable', 'evidence': type(reason).__name__}
    with response:
        headers = response.headers
        # Не сохраняем полные значения X-Powered-By и Set-Cookie.
        banner = ' '.join(headers.get_all('X-Powered-By', []))
        status, version, reason = classify_php(banner)
        if status == 'not_detected':
            cookies = headers.get_all('Set-Cookie', [])
            if any(SESSION_MARK.match(cookie) for cookie in cookies):
                status = 'php_hint'
                reason = 'Наблюдалось имя PHP session cookie (без значения).'
        return {'path': path, 'http_status': response.code,
                'php_version': version, 'status': status, 'evidence': reason}


def probe_port(host, port, scheme, paths, timeout, context, delay):
    """Проверить один порт и все разрешённые пути последовательно.

    Не прекращать проверку после первого PHP-признака: разные пути
    могут обслуживаться разными backend. Недоступный TCP не опрашивается.

    Args:
        host (str): Проверенный хост.
        port (int): TCP-порт.
        scheme (str): http либо https.
        paths (list): Проверенные пути.
        timeout (float): Таймаут операций.
        context (ssl.SSLContext): Настройки TLS.
        delay (float): Пауза перед GET в секундах.
    Returns:
        dict: Результат TCP-проверки и список HTTP-наблюдений.
    """
    reachable, peer, error = tcp_check(host, port, timeout)
    result = {'port': port, 'scheme': scheme, 'tcp_open': reachable,
              'tcp_peer': peer, 'tcp_error': error, 'observations': []}
    if not reachable:
        return result
    for path in paths:
        time.sleep(delay)
        result['observations'].append(make_request(
            host, port, scheme, path, timeout, context
        ))
    return result


def scan(args):
    """Выполнить последовательную инвентаризацию одного хоста.

    Зона — метка места запуска, а не настройка интерфейса. TLS CA задаёт
    пользователь. Применяем только HTTP/1.x средствами urllib.

    Args:
        args (argparse.Namespace): Проверенные параметры запуска.
    Returns:
        dict: Метаданные запуска, DNS-адреса и результаты проверки.
    Raises:
        ValueError: Некорректные параметры.
        OSError: Ошибка DNS, загрузки CA или системной операции.
    """
    host = validate_host(args.target)
    ports = parse_ports(args.ports)
    paths = validate_paths(args.path or list(DEFAULT_PATHS))
    addresses = resolve_host(host)
    context = ssl.create_default_context()
    if args.ca_file:
        context.load_verify_locations(cafile=args.ca_file)
    if args.insecure:
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
    document = {
        'version': VERSION, 'generated_at': datetime.now(timezone.utc)
        .isoformat(), 'host': host, 'zone': args.zone,
        'resolved_ips': addresses, 'cves': list(CVES),
        'tls_verify': not args.insecure, 'paths': paths, 'results': [],
    }
    for port in ports:
        # Auto — соглашение для типовых портов, не определение протокола.
        scheme = args.scheme
        if scheme == 'auto':
            scheme = 'https' if port in TLS_PORTS else 'http'
        document['results'].append(probe_port(
            host, port, scheme, paths, args.timeout, context, args.delay
        ))
    # Дополнительная проверка FastCGI — только TCP connect, без данных.
    if args.fpm_port is not None:
        reachable, peer, error = tcp_check(
            host, args.fpm_port, args.timeout
        )
        document['results'].append({
            'port': args.fpm_port, 'scheme': 'tcp', 'tcp_open': reachable,
            'tcp_peer': peer, 'tcp_error': error, 'observations': []
        })
    return document


def report_rows(document):
    """Преобразовать наблюдения в строки, не теряя закрытые порты.

    Args:
        document (dict): Результат scan().
    Yields:
        dict: Одна строка отчёта с портом, путём и оценкой.
    """
    for result in document['results']:
        base = {key: result[key] for key in ('port', 'scheme', 'tcp_open')}
        if result['observations']:
            for observation in result['observations']:
                yield dict(base, **observation)
        else:
            status = 'tcp_only' if result['tcp_open'] else 'unavailable'
            yield dict(base, path='', http_status=None, php_version=None,
                       status=status, evidence=result['tcp_error'] or '')


def write_reports(document, directory, csv_enabled=False):
    """Сохранить MD, JSON и опциональный CSV.

    Args:
        document (dict): Результат scan().
        directory (str): Каталог для записи отчётов.
        csv_enabled (bool): Дополнительно сохранить CSV.
    Returns:
        list: Пути к созданным файлам (Path).
    Raises:
        OSError: Ошибка создания каталога или записи.
    """
    out = Path(directory)
    out.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    host = document['host'].replace(':', '_')
    stem = out / f'{host}_{document["zone"]}_{stamp}'
    json_path = Path(str(stem) + '.json')
    md_path = Path(str(stem) + '.md')
    rows = list(report_rows(document))
    lines = [
        '# PHP2Shell — сетевая оценка', '',
        f'Хост: {document["host"]}; зона: {document["zone"]}',
        f'Дата UTC: {document["generated_at"]}',
        'DNS: ' + ', '.join(document['resolved_ips']),
        f'Проверка TLS: {document["tls_verify"]}', '',
        '| Порт | Схема | Путь | HTTP | PHP | Оценка |',
        '|---|---|---|---|---|---|',
    ]
    for row in rows:
        cells = [row['port'], row['scheme'], row['path'],
                 row['http_status'], row['php_version'],
                 STATUS_LABELS[row['status']]]
        lines.append('| ' + ' | '.join(
            str(cell if cell is not None else '—').replace('|', '\\|')
            for cell in cells
        ) + ' |')
    lines += ['', 'Баннеры и cookies — косвенные признаки. Проверить '
              'фактический пакет веб-SAPI и бюллетень производителя.',
              'Отсутствие признаков не исключает PHP или CVE.',
              'CVE: ' + ', '.join(CVES)]
    json_path.write_text(json.dumps(document, ensure_ascii=False, indent=2)
                         + '\n', encoding='utf-8')
    md_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    output = [md_path, json_path]
    if csv_enabled:
        csv_path = Path(str(stem) + '.csv')
        with csv_path.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        output.append(csv_path)
    return output


def build_parser():
    """Создать CLI с ограниченной областью проверки и безопасным TLS."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--target', '--host', dest='target')
    parser.add_argument('--ports', '--port', default=None)
    parser.add_argument('--zone', choices=ZONES)
    parser.add_argument('--scheme', choices=('auto', 'http', 'https'),
                        default='auto')
    parser.add_argument('--path', action='append')
    parser.add_argument('--timeout', type=float, default=5)
    parser.add_argument('--delay', type=float, default=0.5)
    parser.add_argument('--ca-file')
    parser.add_argument('--insecure', action='store_true')
    parser.add_argument('--fpm-port', type=int)
    parser.add_argument('--output-dir', default='php_reports')
    parser.add_argument('--csv', action='store_true')
    return parser


def main(argv=None):
    """Запросить параметры, проверить их, выполнить скан и вывести итог.

    Коды завершения: 0 — только баннеры не ниже порогов; 1 — ошибка
    запуска; 2 — потенциально уязвимая версия; 3 — результат неполный.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.target is None:
            args.target = input('Хост (FQDN/IP): ')
            if args.ports is None:
                args.ports = input('Порты [Enter = auto]: ')
            if args.zone is None:
                args.zone = input('Зона [corp/vds/mgmt, Enter=corp]: ')
        args.ports = args.ports or 'auto'
        args.zone = args.zone or 'corp'
        if args.zone not in ZONES:
            raise ValueError('Допустимые зоны: corp, vds, mgmt.')
        if not 0.5 <= args.timeout <= 30 or not MIN_DELAY <= args.delay <= 30:
            raise ValueError('timeout 0.5–30; delay 0.3–30 секунд.')
        if args.fpm_port is not None and not 1 <= args.fpm_port <= 65535:
            raise ValueError('Недопустимый FPM-порт.')
        document = scan(args)
        for row in report_rows(document):
            print(f'{row["scheme"]}:{row["port"]} {row["path"]} '
                  f'{row["php_version"] or "—"}: '
                  f'{STATUS_LABELS[row["status"]]}')
        for path in write_reports(document, args.output_dir, args.csv):
            print('Отчёт:', path)
    except (ValueError, OSError, EOFError) as exc:
        print('Ошибка:', exc, file=sys.stderr)
        return 1
    statuses = {row['status'] for row in report_rows(document)}
    if 'potentially_affected' in statuses:
        return 2
    return 0 if statuses == {'fixed_banner'} else 3


if __name__ == '__main__':
    sys.exit(main())
