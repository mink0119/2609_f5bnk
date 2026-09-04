# 2.18 HTTP URL Rewrite — hostname

## 구성

```mermaid
flowchart LR
  C["Host: coffee.f5bnk.com"] --> VIP[VIP]
  VIP -->|3xx 없음, upstream Host=tea.f5bnk.com| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 클라이언트는 200, redirect 없음

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- 3xx/Location 없음
- 백엔드가 받은 Host는 `tea.f5bnk.com`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

client redirect 없이 upstream Host만 바꿉니다.
