"""Локальные тесты классификации PHP и неразрушающей диагностики."""

import argparse
import json
import ssl
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import php_cve_scanner as scanner


class Handler(BaseHTTPRequestHandler):
    """Имитировать разные баннеры, cookie и перенаправление."""

    def do_GET(self):
        """Вернуть заданный тестовый ответ без выполнения PHP."""
        self.server.paths.append(self.path)
        code = 302 if self.path == '/redirect' else 200
        self.send_response(code)
        if self.path == '/':
            self.send_header('Set-Cookie', 'PHPSESSID=SECRET_TEST_VALUE')
        elif self.path == '/index.php':
            self.send_header('X-Powered-By', 'PHP/8.2.34')
        elif self.path == '/redirect':
            self.send_header('Location', '/forbidden-follow')
        elif self.path == '/patched':
            self.send_header('X-Powered-By', 'PHP/8.2.35')
        self.end_headers()

    def log_message(self, *_args):
        """Не записывать запросы в stderr при выполнении тестов."""


class ScannerTests(unittest.TestCase):
    """Проверить обработку версий, параметры и локальный HTTP."""

    def test_versions(self):
        """Различать исправленные, старые и неопределённые сборки."""
        for branch, patch in scanner.FIXED.items():
            prefix = 'PHP/{}.{}.'.format(*branch)
            for delta, expected in [(-1, 'potentially_affected'),
                                    (0, 'fixed_banner'), (1, 'fixed_banner')]:
                with self.subTest(branch=branch, delta=delta):
                    self.assertEqual(scanner.classify_php(
                        prefix + str(patch + delta))[0], expected)
        for version in ('PHP/8.2', 'PHP/8.2.35RC1', 'PHP/7.4.33',
                        'PHP/9.0.0', 'PHP/8.2.34-1ubuntu1'):
            self.assertEqual(scanner.classify_php(version)[0],
                             'unknown_build')
        self.assertEqual(scanner.classify_php('OTHER/8.2.34')[0],
                         'not_detected')
        self.assertEqual(scanner.classify_php('PHP')[0], 'php_hint')

    def test_validation(self):
        """Отклонять CIDR, URL, неверные порты и пути."""
        self.assertEqual(scanner.parse_ports('443,443,80'), [443, 80])
        self.assertEqual(scanner.parse_ports(''),
                         list(scanner.DEFAULT_PORTS))
        for host in ('10.0.0.0/24', 'https://example.test', 'foo:443'):
            with self.assertRaises(ValueError):
                scanner.validate_host(host)
        for ports in ('0', '65536', 'hello'):
            with self.assertRaises(ValueError):
                scanner.parse_ports(ports)
        for path in ('//example.test/', '/a?b=1', '/a#x', '/%0a'):
            with self.assertRaises(ValueError):
                scanner.validate_paths([path])

    def test_local_http_and_reports(self):
        """Не переходить по редиректу и не сохранять секрет cookie."""
        with HTTPServer(('127.0.0.1', 0), Handler) as server:
            server.paths = []
            thread = threading.Thread(target=server.serve_forever,
                                      daemon=True)
            thread.start()
            try:
                args = argparse.Namespace(
                    target='127.0.0.1', ports=str(server.server_port),
                    zone='corp', scheme='http', timeout=2, delay=0.3,
                    path=['/', '/index.php', '/redirect', '/patched'],
                    ca_file=None, insecure=False, fpm_port=None)
                result = scanner.scan(args)
                rows = list(scanner.report_rows(result))
                self.assertEqual([r['status'] for r in rows], [
                    'php_hint', 'potentially_affected', 'not_detected',
                    'fixed_banner'])
                self.assertEqual(rows[2]['http_status'], 302)
                self.assertNotIn('/forbidden-follow', server.paths)
                with tempfile.TemporaryDirectory() as directory:
                    paths = scanner.write_reports(result, directory, True)
                    self.assertEqual(len(paths), 3)
                    for path in paths:
                        self.assertNotIn('SECRET_TEST_VALUE',
                                         path.read_text(encoding='utf-8'))
                    doc = json.loads(Path(paths[1]).read_text('utf-8'))
                    self.assertEqual(doc, result)
            finally:
                server.shutdown()
                thread.join()

    def test_closed_port(self):
        """Зафиксировать ошибку TCP без отправки HTTP на закрытый порт."""
        import socket

        with socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            port = sock.getsockname()[1]
            result = scanner.probe_port(
                '127.0.0.1', port, 'http', ['/'], 1,
                ssl.create_default_context(), 0.3)
            self.assertFalse(result['tcp_open'])
            self.assertEqual(result['observations'], [])


if __name__ == '__main__':
    unittest.main()
