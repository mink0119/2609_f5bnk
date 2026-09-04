# 2.30 HTTP CORS — allowOrigins / allowCredentials

## 구성

```mermaid
flowchart LR
  C["Origin: shop.f5bnk.com"] --> VIP[VIP]
  VIP -->|Allow-Origin + Credentials| C
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 허용 Origin

```bash
curl -sS -D - -o /tmp/gw-body -H 'Origin: https://shop.f5bnk.com' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- `Access-Control-Allow-Origin: https://shop.f5bnk.com`
- `Access-Control-Allow-Credentials: true`
- Allow-Origin 이 `*` 이면 실패 (credentials=true)

### 2. 비허용 Origin

```bash
curl -sS -D - -o /tmp/gw-body -H 'Origin: https://evil.example.com' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- `Access-Control-Allow-Origin: https://evil.example.com` 이면 실패

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
