# 2.42 HTTP Retry — backoff

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|최소 100ms 대기 후 retry| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200

### 2. 재시도 간격

```bash
echo '503 연속 시 로그 timestamp 간격 >= 100ms. request/backendRequest timeout과 함께 종료'
```

**기대 응답**
- 최소 backoff 100ms
- 전체는 request 5s를 넘지 않음

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
