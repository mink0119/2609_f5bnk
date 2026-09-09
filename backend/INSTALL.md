# 백엔드 서버 설치 (`192.168.48.254`)

이 디렉터리(`backend/`)가 **현재 live 서버와 같은 설정**이다.  
2026-09-09 기준 `tea-svc` (`192.168.48.254`) 와 nginx vhost·unit·gRPC/UDP 소스를 대조했다. 빠진 것은 `/etc/default/poc-*` 와 netplan·pip `--target` 뿐이었고, 이 레포에 넣었다.

대상 호스트는 마스터가 아니다. 마스터에서 레포를 복사한 뒤 **백엔드에서** 아래를 실행한다.  
`coffee.conf` 를 다른 내용으로 덮어쓰지 말라는 제약은 **이미 떠 있는 서버를 고칠 때**다. 서버를 처음부터 다시 만들 때는 이 파일을 그대로 쓴다.

## 1. 호스트

| | live |
|---|---|
| hostname | `tea-svc` |
| OS | Ubuntu 22.04, Python 3.10.12, nginx 1.18.0 |
| 관리 IP | `192.168.48.254` (`ens33`) |
| Pool IP | `30.0.0.10` coffee, `30.0.0.11` tea, `30.0.0.12` canary (`ens160`) |
| SSH | `root@192.168.48.254` |

NIC 이름이 다르면 netplan 의 `ens33` / `ens160` 만 맞추고 주소는 그대로 둔다.

```bash
apt-get update
apt-get install -y nginx python3 python3-pip python3-venv
# sites-enabled/default 는 쓰지 않는다. nginx.conf 가 conf.d 만 include.
rm -f /etc/nginx/sites-enabled/default
```

IP:

```bash
cp netplan/01-network-manager-all.yaml /etc/netplan/01-network-manager-all.yaml
chmod 600 /etc/netplan/01-network-manager-all.yaml
netplan apply
ip -4 addr
```

## 2. 레포 → 서버 경로

레포 루트는 마스터 `/root/bnk/web/poc`. 백엔드에 복사할 때 `backend/` 를 기준으로 한다.

```bash
# 예: 마스터에서
scp -r /root/bnk/web/poc/backend root@192.168.48.254:/root/poc-backend
# 이후 백엔드
cd /root/poc-backend
```

| 레포 | 서버 |
|---|---|
| `nginx.conf` | `/etc/nginx/nginx.conf` |
| `conf.d/*.conf` | `/etc/nginx/conf.d/` |
| `poc-delay.py` | `/etc/nginx/poc-delay.py` |
| `poc-slow.txt` | `/etc/nginx/poc-slow.txt` |
| `poc-delay.service` | `/etc/systemd/system/poc-delay.service` |
| `certs/coffee.crt` `.key` `tea.crt` `.key` `ca.crt` | `/etc/nginx/poc-certs/` |
| `grpc/hello_*.py` `hello.proto` `hello_server.py` | `/opt/poc/grpc/` |
| `grpc/hello-server.service` | `/etc/systemd/system/poc-grpc@.service` |
| `udp/echo.py` | `/opt/poc/udp/echo.py` |
| `udp/udp-echo.service` | `/etc/systemd/system/poc-udp@.service` |
| `default/poc-grpc-*` | `/etc/default/poc-grpc-*` |
| `default/poc-udp-*` | `/etc/default/poc-udp-*` |

`certs/ca.key` `gw-terminate.*` 는 Gateway Secret / BackendTLSPolicy 용. nginx `poc-certs` 에는 넣지 않는다.  
`live-snapshot/` 은 예전 덤프. 설치에 쓰지 않는다.

## 3. nginx HTTP + TLS + delay

```bash
mkdir -p /etc/nginx/conf.d /etc/nginx/poc-certs
cp nginx.conf /etc/nginx/nginx.conf
cp conf.d/coffee.conf conf.d/tea.conf conf.d/canary.conf \
   conf.d/coffee-tls.conf conf.d/tea-tls.conf /etc/nginx/conf.d/
cp poc-delay.py /etc/nginx/poc-delay.py
chmod +x /etc/nginx/poc-delay.py
cp poc-slow.txt /etc/nginx/poc-slow.txt
cp certs/coffee.crt certs/coffee.key certs/tea.crt certs/tea.key certs/ca.crt \
   /etc/nginx/poc-certs/
chmod 600 /etc/nginx/poc-certs/*.key

touch /var/log/nginx/poc-access.log
chown www-data:www-data /var/log/nginx/poc-access.log

cp poc-delay.service /etc/systemd/system/poc-delay.service
systemctl daemon-reload
systemctl enable --now poc-delay.service
nginx -t && systemctl reload nginx
systemctl enable nginx
```

역할:

| listen | 파일 | body / 용도 |
|---|---|---|
| `30.0.0.10:80` | `coffee.conf` | `COFFEE SERVER - 30.0.0.10`. `/fail` 503, `/fail404` 404, `/fail500` 500, `/delay/` → `127.0.0.1:18080`, `/slow` |
| `30.0.0.11:80` | `tea.conf` | `TEA SERVER - 30.0.0.11`. `/delay/` 동일 helper |
| `30.0.0.12:80` | `canary.conf` | `HTTPBIN CANARY SERVER - 30.0.0.12`. `/auth` 200, `/auth/deny` 401 |
| `30.0.0.10:443` | `coffee-tls.conf` | `COFFEE TLS - 30.0.0.10` |
| `30.0.0.11:443` | `tea-tls.conf` | `TEA TLS - 30.0.0.11` |

`poc-delay` 는 `Restart=always`. coffee·tea 둘 다 `/delay/` 를 이 프로세스에 보낸다.

## 4. gRPC `:50051`

nginx 와 별 프로세스. 패키지는 시스템 site-packages 가 아니라 `/opt/poc/pydeps`.

```bash
mkdir -p /opt/poc/grpc /opt/poc/pydeps
python3 -m pip install --target /opt/poc/pydeps -r grpc/requirements.txt
# hello_pb2*.py 는 레포에 있다. 다시 만들려면:
# PYTHONPATH=/opt/poc/pydeps python3 -m grpc_tools.protoc -I grpc --python_out=grpc --grpc_python_out=. grpc/hello.proto
# (cwd 를 grpc/ 로 두고 생성하는 편이 import 가 맞다)

cp grpc/hello.proto grpc/hello_server.py grpc/hello_pb2.py grpc/hello_pb2_grpc.py /opt/poc/grpc/
chmod +x /opt/poc/grpc/hello_server.py
cp grpc/hello-server.service /etc/systemd/system/poc-grpc@.service
cp default/poc-grpc-coffee /etc/default/poc-grpc-coffee
cp default/poc-grpc-tea /etc/default/poc-grpc-tea
cp default/poc-grpc-canary /etc/default/poc-grpc-canary
systemctl daemon-reload
systemctl enable --now poc-grpc@coffee poc-grpc@tea poc-grpc@canary
```

`SayHello` 는 요청 metadata `x-poc-add` 가 있으면 trailer `x-echo-x-poc-add` 로 echo (3.12).

## 5. UDP `:9053`

호스트 `named` 가 :53 을 쓰므로 9053 이다.

```bash
mkdir -p /opt/poc/udp
cp udp/echo.py /opt/poc/udp/echo.py
chmod +x /opt/poc/udp/echo.py
cp udp/udp-echo.service /etc/systemd/system/poc-udp@.service
cp default/poc-udp-coffee /etc/default/poc-udp-coffee
cp default/poc-udp-tea /etc/default/poc-udp-tea
systemctl daemon-reload
systemctl enable --now poc-udp@coffee poc-udp@tea
```

## 6. 확인

백엔드 로컬 또는 ncurity 에서 **Pool IP 직접**. VIP 가 아니다.

```bash
systemctl is-active nginx poc-delay \
  poc-grpc@coffee poc-grpc@tea poc-grpc@canary \
  poc-udp@coffee poc-udp@tea

curl -sS http://30.0.0.10/ ; echo
curl -sS http://30.0.0.11/ ; echo
curl -sS http://30.0.0.12/ ; echo
curl -sS http://30.0.0.12/auth ; echo
curl -sk https://30.0.0.10/ ; echo
curl -sk https://30.0.0.11/ ; echo
curl -sS http://30.0.0.10/fail -o /dev/null -w '%{http_code}\n'
curl -sS --max-time 2 http://30.0.0.10/delay/0 ; echo

# gRPC 는 ncurity $HOME/poc-grpc (3.10 README)
# "$HOME/poc-grpc/grpcurl" -plaintext -import-path "$HOME/poc-grpc" -proto hello.proto \
#   -d '{"name":"BNK"}' 30.0.0.10:50051 hello.HelloService/SayHello

echo -n ping | nc -u -w 2 30.0.0.10 9053 ; echo
```

기대 body:

- `COFFEE SERVER - 30.0.0.10`
- `TEA SERVER - 30.0.0.11`
- `HTTPBIN CANARY SERVER - 30.0.0.12`
- `AUTH OK`
- `COFFEE TLS - 30.0.0.10` / `TEA TLS - 30.0.0.11`
- `/fail` → 503
- `DELAYED 0.0s - 30.0.0.10` (`/delay/` 는 helper 가 항상 이 문자열)
- gRPC: `COFFEE GRPC - 30.0.0.10 hello BNK`
- UDP: `COFFEE UDP - 30.0.0.10 ping`

## 7. 코드만 바꾼 뒤

```bash
# hello_server.py 등
cp grpc/hello_server.py /opt/poc/grpc/
systemctl restart poc-grpc@coffee poc-grpc@tea poc-grpc@canary

# nginx vhost
cp conf.d/*.conf /etc/nginx/conf.d/
nginx -t && systemctl reload nginx

# delay helper
cp poc-delay.py /etc/nginx/poc-delay.py
systemctl restart poc-delay
```
