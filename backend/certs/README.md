# PoC TLS certs (draft — do not overwrite live HTTP vhosts)

사설 CA 와 `coffee.f5bnk.com` / `tea.f5bnk.com` 서버 인증서입니다.

| 파일 | 용도 |
|---|---|
| `ca.crt` / `ca.key` | BackendTLSPolicy ConfigMap `backend-ca` |
| `coffee.crt` / `coffee.key` | 30.0.0.10:443 SAN=coffee.f5bnk.com |
| `tea.crt` / `tea.key` | 30.0.0.11:443 SAN=tea.f5bnk.com (3.7 mismatch) |
| `gw-terminate.crt` / `.key` | Gateway Secret `web-tls-cert` (3.5, coffee와 동일) |

재발급:

```bash
./gen-poc-certs.sh
```

HTTP 2.x 테스트가 끝난 뒤에만 백엔드에 복사합니다. `coffee.conf` 는 덮어쓰지 않습니다. 서버 전체 재설치는 **`../INSTALL.md`**.

```bash
# later, on 192.168.48.254
mkdir -p /etc/nginx/poc-certs
cp coffee.crt coffee.key tea.crt tea.key ca.crt /etc/nginx/poc-certs/
cp ../conf.d/coffee-tls.conf ../conf.d/tea-tls.conf /etc/nginx/conf.d/
nginx -t && systemctl reload nginx
```
