# 2.24 Response Header Modifier — set

## 구성

```mermaid
flowchart LR
  P1[coffee-pool Server: nginx] --> VIP[VIP]
  VIP -->|"set Server: f5-bnk-poc"| C[Client]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 응답 Server 덮어씀

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- 응답 헤더 `Server: f5-bnk-poc` (원본 nginx 값이 아님)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
