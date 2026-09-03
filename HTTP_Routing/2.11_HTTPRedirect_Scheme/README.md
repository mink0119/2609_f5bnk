# 2.11 HTTP Redirect — scheme

## 구성

```mermaid
flowchart LR
  C[Client http] --> VIP[VIP :80]
  VIP -->|RequestRedirect scheme https| R["301 Location: https://coffee.f5bnk.com/..."]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. http → https

```bash
curl -sS -D - -o /tmp/gw-body --max-redirs 0 -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 301
- Location 스킴이 `https://`
- 백엔드로 전달되지 않음 (redirect filter only)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
