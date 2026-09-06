# 3.11 GRPCRoute — headers Exact / RegularExpression

gRPC metadata header 로 backend 를 나눕니다.

## 구성

```mermaid
flowchart LR
  C[gRPC] --> GW[http-gw]
  GW -->|env:canary Exact| P3[httpbin-pool :50051]
  GW -->|"env ~ canary-.* Regex"| P2[tea-pool :50051]
  GW -->|그 외| P1[coffee-pool :50051]
```

## 적용

```bash
kubectl apply -f gw-grpc-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. Exact

```bash
grpcurl -plaintext -authority grpc.f5bnk.com \
  -H 'env: canary' 40.30.20.20:80 hello.HelloService/SayHello
```

**기대 응답**
- httpbin-pool (`CANARY GRPC - 30.0.0.12`)

### 2. RegularExpression

```bash
grpcurl -plaintext -authority grpc.f5bnk.com \
  -H 'env: canary-01' 40.30.20.20:80 hello.HelloService/SayHello
```

**기대 응답**
- tea-pool (`TEA GRPC - 30.0.0.11`)
- 구현체가 header regex 미지원이면 해당 rule Accepted=False / UnsupportedValue

### 3. 헤더 없음

```bash
grpcurl -plaintext -authority grpc.f5bnk.com \
  40.30.20.20:80 hello.HelloService/SayHello
```

**기대 응답**
- coffee-pool (`COFFEE GRPC - 30.0.0.10`)

## 정리

```bash
kubectl delete -f gw-grpc-route.yaml
```

## live 결과

Accepted=True. grpcurl `-H env:` 메타데이터는 백엔드 로그에 도달했으나 모든 RPC가 첫 rule(canary). gRPC header iRule 없음.
