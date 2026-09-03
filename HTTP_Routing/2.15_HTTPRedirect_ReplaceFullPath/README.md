# 2.15 HTTP Redirect — path ReplaceFullPath

## 구성

```mermaid
flowchart LR
  C["GET /old/anything"] --> VIP[VIP]
  VIP --> R["301 Location path = /new"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 전체 path 교체

```bash
curl -sS -D - -o /tmp/gw-body --max-redirs 0 -H 'Host: coffee.f5bnk.com' http://40.30.20.20/old/anything; echo
```

**기대 응답**
- HTTP/1.1 301
- Location path 가 `/new` (뒤에 /anything 이 붙지 않음)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
