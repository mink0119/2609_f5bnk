# PoC gRPC HelloService

`hello.HelloService/SayHello` 와 `SayGoodbye` 를 30.0.0.10/11/12:50051 에 올립니다. nginx HTTP :80 과는 별 프로세스입니다.

| 역할 | 호스트 | 하는 일 |
|---|---|---|
| kubectl / 레포 | 마스터 `/root/bnk/web/poc` | YAML apply |
| 트래픽 | 클라이언트 **ncurity** (`~/`) | `grpcurl`. 레포 없음 |
| gRPC 서버 | `192.168.48.254` | coffee/tea/canary `:50051` |

## 백엔드 설치 (`192.168.48.254`)

HTTP 2.x 가 끝난 뒤에만 설치합니다. `nginx` 재시작·`coffee.conf` 덮어쓰기는 하지 않습니다.

```bash
python3 -m pip install -r requirements.txt
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. hello.proto

mkdir -p /opt/poc/grpc
cp hello.proto hello_server.py hello_pb2.py hello_pb2_grpc.py /opt/poc/grpc/

printf 'BIND_ADDR=30.0.0.10\nBIND_PORT=50051\nPOOL_NAME=COFFEE GRPC - 30.0.0.10\n' > /etc/default/poc-grpc-coffee
printf 'BIND_ADDR=30.0.0.11\nBIND_PORT=50051\nPOOL_NAME=TEA GRPC - 30.0.0.11\n' > /etc/default/poc-grpc-tea
printf 'BIND_ADDR=30.0.0.12\nBIND_PORT=50051\nPOOL_NAME=CANARY GRPC - 30.0.0.12\n' > /etc/default/poc-grpc-canary

cp hello-server.service /etc/systemd/system/poc-grpc@.service
systemctl daemon-reload
systemctl enable --now poc-grpc@coffee poc-grpc@tea poc-grpc@canary
# 코드 바꾼 뒤
systemctl restart poc-grpc@coffee poc-grpc@tea poc-grpc@canary
```

## 클라이언트 `ncurity` — 3.10 README 블록 한 번

PATH `grpcurl` (snap) 은 `~`/`/tmp` 를 못 읽습니다. `$HOME/poc-grpc/grpcurl` 과 `hello.proto` 를 같이 둡니다.

```bash
"$HOME/poc-grpc/grpcurl" -plaintext \
  -import-path "$HOME/poc-grpc" -proto hello.proto \
  -d '{"name":"BNK"}' 30.0.0.10:50051 hello.HelloService/SayHello
```
