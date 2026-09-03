# 2.39 HTTP Retries — attempts

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|503, attempts 3| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상

```bash
curl -sS -D - -o /tmp/gw-body  -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. attempts=3

```bash
echo '백엔드가 계속 503이면 최대 3번 재시도 후 에러'
```

**기대 응답**
- 백엔드 로그 요청 수 <= 1 + 3
- 모두 실패하면 클라이언트에 502/503

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
