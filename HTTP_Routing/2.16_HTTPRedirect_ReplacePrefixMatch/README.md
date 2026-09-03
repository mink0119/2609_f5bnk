# 2.16 HTTP Redirect — path ReplacePrefixMatch

## 구성

```mermaid
flowchart LR
  C["GET /api/users"] --> VIP[VIP]
  VIP --> R["301 Location path = /v2/users"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. prefix만 교체

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/api/users
```

**기대 응답**
- HTTP/1.1 301
- Location path 가 `/v2/users` (`/api` → `/v2`, 나머지 유지)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
