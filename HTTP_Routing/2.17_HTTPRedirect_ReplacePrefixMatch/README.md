# 2.17 HTTP Redirect — path ReplacePrefixMatch

## 구성

```mermaid
flowchart LR
  C["GET /old/child"] --> VIP[VIP]
  VIP --> R["301 Location: /new/child"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. prefix만 교체, suffix 유지

```bash
curl -sS -D - -o /tmp/gw-body --max-redirs 0  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old/child; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 301
- Location path가 `/new/child`

### 2. 깊은 suffix

```bash
curl -sS -D - -o /tmp/gw-body --max-redirs 0  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old/child/item; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 301
- Location path가 `/new/child/item`

### 3. prefix만

```bash
curl -sS -D - -o /tmp/gw-body --max-redirs 0  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/old; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 301
- Location path가 `/new`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
