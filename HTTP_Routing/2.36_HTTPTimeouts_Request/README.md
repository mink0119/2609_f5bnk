# 2.36 HTTP Timeouts — request

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|timeouts.request 5s| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상 응답 (5초 이내)

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. 타임아웃

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/slow
```

**기대 응답**
- 느린 백엔드가 있을 때 `timeouts.request: 5s` 초과 시 클라이언트에 504 (또는 구현 timeout 코드)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
