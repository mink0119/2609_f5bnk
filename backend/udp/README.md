# PoC UDP echo

30.0.0.10/11:9053. 호스트 `named` 가 이미 :53 을 쓰므로 53 은 피합니다.

서버 전체 재설치는 **`../INSTALL.md`**.

HTTP 2.x 가 끝난 뒤에만:

```bash
# on 192.168.48.254 — later
mkdir -p /opt/poc/udp
cp echo.py /opt/poc/udp/
cp ../default/poc-udp-coffee /etc/default/poc-udp-coffee
cp ../default/poc-udp-tea /etc/default/poc-udp-tea
cp udp-echo.service /etc/systemd/system/poc-udp@.service
systemctl daemon-reload
systemctl enable --now poc-udp@coffee poc-udp@tea
```
