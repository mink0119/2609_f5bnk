# PoC gRPC HelloService (draft — do not install during HTTP 2.x)

`hello.HelloService/SayHello` 를 30.0.0.10/11/12:50051 에 올립니다. nginx HTTP :80 과는 별 프로세스입니다.

HTTP 2.x 가 끝난 뒤에만 백엔드에 설치합니다.

```bash
# on 192.168.48.254 — later
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
```

로컬 확인:

```bash
grpcurl -plaintext 30.0.0.10:50051 hello.HelloService/SayHello
```

`nginx` 재시작·`coffee.conf` 덮어쓰기는 하지 않습니다.
