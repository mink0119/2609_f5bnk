# 2.21 Request Header Modifier — set

## 구성

```mermaid
flowchart LR
  C["X-PoC-Set: client"] --> VIP[VIP]
  VIP -->|"set X-PoC-Set: overwritten"| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. set은 덮어씀

```bash
curl -sS -D - -o /tmp/gw-body -H 'X-PoC-Set: client' -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- 백엔드가 받은 `X-PoC-Set` 값은 `overwritten` (client 아님)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
