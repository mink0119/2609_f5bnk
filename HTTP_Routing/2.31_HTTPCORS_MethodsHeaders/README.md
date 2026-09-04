# 2.31 HTTP CORS — allowMethods / allowHeaders

## 구성

```mermaid
flowchart LR
  C[OPTIONS preflight] --> VIP[VIP]
  VIP -->|Allow-Methods / Allow-Headers| C
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 허용 preflight

```bash
curl -sS -D - -o /tmp/gw-body -X OPTIONS -H 'Origin: https://shop.f5bnk.com' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: Content-Type, Authorization' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- 200 또는 204
- `Access-Control-Allow-Methods` 에 GET, POST
- `Access-Control-Allow-Headers` 에 Content-Type, Authorization

### 2. 비허용 method

```bash
curl -sS -D - -o /tmp/gw-body -X OPTIONS -H 'Origin: https://shop.f5bnk.com' -H 'Access-Control-Request-Method: DELETE' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- DELETE가 Allow-Methods에 없거나 preflight 거부

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
