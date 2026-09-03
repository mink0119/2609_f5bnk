# 2.18 HTTP URL Rewrite — ReplaceFullPath

## 구성

```mermaid
flowchart LR
  C["GET /old/x"] --> VIP[VIP]
  VIP -->|backend path /rewritten| P1["coffee-pool 30.0.0.10"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 클라이언트 URL은 /old

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old/x
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10` (coffee 서버가 / 만 허용하면 다른 body/404 일 수 있음)
- 백엔드가 받은 path는 `/rewritten`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
