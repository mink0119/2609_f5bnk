# 3.12 GRPCRoute — request/response modifier

## 구성

```mermaid
flowchart LR
  C[gRPC] --> GW[http-gw]
  GW -->|add X-PoC-Add| P1[coffee-pool]
  P1 -->|add X-PoC-Res-Add| C
```

## 적용

```bash
kubectl apply -f gw-grpc-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 헤더 수정 후 호출

```bash
grpcurl -plaintext -authority grpc.f5bnk.com -v 40.30.20.20:80 hello.HelloService/SayHello
```

**기대 응답**
- 백엔드가 `X-PoC-Add: added` 수신
- 클라이언트 응답 트레일러/헤더에 `X-PoC-Res-Add: added`

## 정리

```bash
kubectl delete -f gw-grpc-route.yaml
```
