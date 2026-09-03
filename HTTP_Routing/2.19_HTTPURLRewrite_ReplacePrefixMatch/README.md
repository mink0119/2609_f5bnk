# 2.19 HTTP URL Rewrite — ReplacePrefixMatch

## 구성

```mermaid
flowchart LR
  C["GET /api/users"] --> VIP[VIP]
  VIP -->|backend path /v2/users| P1["coffee-pool 30.0.0.10"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. prefix rewrite

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/api/users
```

**기대 응답**
- HTTP/1.1 200 (또는 백엔드 path 처리 결과)
- 백엔드가 받은 path는 `/v2/users`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
