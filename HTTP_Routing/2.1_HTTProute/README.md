# 2.1 HTTPRoute — 기본 전달

## 구성

```mermaid
flowchart LR
  C[Client 40.0.0.x] --> VIP["VIP 40.30.20.20 :80"]
  VIP -->|Host coffee.f5bnk.com<br/>Path /login| P1["coffee-pool 30.0.0.10"]
  VIP -->|Host tea.f5bnk.com<br/>header env:canary| P3["httpbin-pool 30.0.0.12"]
  VIP -->|Host tea.f5bnk.com<br/>그 외 /| P2["tea-pool 30.0.0.11"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. coffee /login

```bash
curl -sS -D - -o /tmp/gw-body  -H 'Host: coffee.f5bnk.com' http://40.30.20.20/login; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. coffee / 는 매칭 없음

```bash
curl -sS -D - -o /tmp/gw-body  -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 404 (Gateway에서 매칭되는 rule 없음)

### 3. tea 기본

```bash
curl -sS -D - -o /tmp/gw-body  -H 'Host: tea.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `TEA SERVER - 30.0.0.11`

### 4. tea canary 헤더

```bash
curl -sS -D - -o /tmp/gw-body -H 'env: canary' -H 'Host: tea.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `HTTPBIN CANARY SERVER - 30.0.0.12`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
