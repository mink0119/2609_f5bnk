# 2.20 HTTP URL Rewrite — ReplacePrefixMatch

## 구성

```mermaid
flowchart LR
  C["GET /old/child"] --> VIP[VIP]
  VIP -->|backend /new/child| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. prefix만 교체

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old/child; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- 3xx 없음
- 백엔드 path는 `/new/child` (suffix 유지)

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

같은 rule에 RequestRedirect와 URLRewrite를 같이 쓰면 구현체가 거부할 수 있습니다.
