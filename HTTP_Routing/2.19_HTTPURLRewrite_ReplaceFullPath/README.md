# 2.19 HTTP URL Rewrite — ReplaceFullPath

## 구성

```mermaid
flowchart LR
  C["GET /old/child?x=1"] --> VIP[VIP]
  VIP -->|backend path /rewritten?x=1| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 전체 path 교체, query 보존

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old/child?x=1; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200 (또는 백엔드 path 처리 결과)
- 3xx 없음
- 백엔드 path는 `/rewritten`, query `x=1` 유지

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
