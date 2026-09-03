# 2.10 HTTPRoute Match — method

## 구성

```mermaid
flowchart LR
  C[Client Host coffee.f5bnk.com] --> VIP[VIP]
  VIP -->|GET| P1["coffee-pool 30.0.0.10"]
  VIP -->|POST| P2["tea-pool 30.0.0.11"]
  VIP -->|PUT 등| X[404]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. GET

```bash
curl -sS -D - -o /tmp/gw-body -X GET -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. POST

```bash
curl -sS -D - -o /tmp/gw-body -X POST -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `TEA SERVER - 30.0.0.11`

### 3. 매칭 안 되는 method

```bash
curl -sS -D - -o /tmp/gw-body -X PUT -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 404

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
