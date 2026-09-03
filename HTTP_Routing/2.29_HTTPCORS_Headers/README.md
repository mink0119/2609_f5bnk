# 2.29 HTTP CORS — allowHeaders / exposeHeaders

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|Allow-Headers / Expose-Headers| C
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. preflight 허용 헤더

```bash
curl -sS -D - -o /tmp/gw-body -X OPTIONS \
  -H 'Host: coffee.f5bnk.com' \
  -H 'Origin: https://shop.f5bnk.com' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: Content-Type, Authorization' \
  http://40.30.20.20/; echo
```

**기대 응답**
- `Access-Control-Allow-Headers` 에 Content-Type, Authorization, env

### 2. 실제 요청 expose

```bash
curl -sS -D - -o /tmp/gw-body -H 'Origin: https://shop.f5bnk.com' -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- `Access-Control-Expose-Headers` 에 X-Request-Id, X-PoC-Res-Add

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
