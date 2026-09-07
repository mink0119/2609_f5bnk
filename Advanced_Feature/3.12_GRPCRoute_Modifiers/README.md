# 3.12 GRPCRoute — request/response modifier

gRPC 요청·응답 metadata header 를 추가합니다.

## 구성

```mermaid
flowchart LR
  C[gRPC] --> GW[http-gw]
  GW -->|add X-PoC-Add| P1[coffee-pool :50051]
  P1 -->|add X-PoC-Res-Add| C
```

## 적용

```bash
kubectl apply -f gw-grpc-route.yaml
```

명령은 클라이언트 **ncurity** 에서 실행합니다.  
`"$HOME/poc-grpc"` 는 3.10 README 블록을 한 번 실행해 둡니다.

## 클라이언트 검증

### 1. 헤더 수정 후 호출

```bash
"$HOME/poc-grpc/grpcurl" -plaintext -authority grpc.f5bnk.com -v \
  -import-path "$HOME/poc-grpc" -proto hello.proto -d '{"name":"BNK"}' \
  40.30.20.20:80 hello.HelloService/SayHello
```

**기대 응답**
- 백엔드가 `X-PoC-Add: added` 수신 (서버 reply 또는 로그)
- 클라이언트 응답 헤더/트레일러에 `X-PoC-Res-Add: added`

## 정리

```bash
kubectl delete -f gw-grpc-route.yaml
```

## live 결과

Accepted=True. VIP → coffee 200 (`COFFEE GRPC - 30.0.0.10 hello BNK`).
`grpcurl -v`: 응답 헤더에 `X-PoC-Res-Add` 없음, trailer 비어 있음 (`x-echo-x-poc-add` 없음 → 요청 add도 미적용).
BNK GRPCRoute `filters` 미지원. gRPC iRule 없음.
