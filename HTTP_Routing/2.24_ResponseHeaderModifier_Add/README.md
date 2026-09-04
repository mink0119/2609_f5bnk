# 2.24 Response Header Modifier — add

## 구성

```mermaid
flowchart LR
  P1[coffee-pool] --> VIP[VIP]
  VIP -->|"add X-PoC-Res-Add: added"| C[Client]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 응답에 헤더 추가

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- `X-PoC-Res-Add: added`
- 백엔드 원본 헤더는 유지

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
