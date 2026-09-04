# PoC UDP echo (draft — do not install during HTTP 2.x)

30.0.0.10/11:9053. 호스트 `named` 가 이미 :53 을 쓰므로 53 은 피합니다.

HTTP 2.x 가 끝난 뒤에만:

```bash
# on 192.168.48.254 — later
mkdir -p /opt/poc/udp
cp echo.py /opt/poc/udp/
printf 'BIND_ADDR=30.0.0.10\nBIND_PORT=9053\nPOOL_NAME=COFFEE UDP - 30.0.0.10\n' > /etc/default/poc-udp-coffee
printf 'BIND_ADDR=30.0.0.11\nBIND_PORT=9053\nPOOL_NAME=TEA UDP - 30.0.0.11\n' > /etc/default/poc-udp-tea
cp udp-echo.service /etc/systemd/system/poc-udp@.service
systemctl daemon-reload
systemctl enable --now poc-udp@coffee poc-udp@tea
```
