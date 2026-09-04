# 2.38 HTTP Timeouts — request

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|request 5s| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상 (5초 이내)

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. 지연 시

```bash
echo '백엔드가 5초 넘기면 Gateway timeout (보통 504). 0s는 timeout 비활성화'
```

**기대 응답**
- > 5s 지연이면 timeout
- `request: 0s` 는 timeout 끔

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
