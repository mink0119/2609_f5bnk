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
curl -sS -D - -o /tmp/gw-body  -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. 타임아웃 동작

```bash
echo '백엔드가 5초 이상 지연되면 Gateway가 504/timeout 을 반환해야 함'
```

**기대 응답**
- 느린 백엔드가 있을 때 `timeouts.request: 5s` 초과 시 클라이언트에 504 (또는 구현 timeout 코드)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
