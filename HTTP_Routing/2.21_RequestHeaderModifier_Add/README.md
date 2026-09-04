# 2.21 Request Header Modifier — add

## 구성

```mermaid
flowchart LR
  C["X-PoC-Add 없음"] --> VIP[VIP]
  VIP -->|"add X-PoC-Add: added"| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

`add`는 요청에 해당 헤더가 **없을 때만** 추가합니다. 이미 있으면 그대로 두고, `set`(2.22)처럼 덮어쓰지 않습니다.

백엔드 echo: `X-Echo-X-PoC-Add`

### 1. 헤더 없음 → 추가

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- `X-Echo-X-PoC-Add: added`

### 2. 헤더 있음 → 추가하지 않음 (overwrite 없음)

```bash
curl -sS -D - -o /tmp/gw-body -H 'X-PoC-Add: client' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- `X-Echo-X-PoC-Add: client`
- `added` 로 바뀌지 않음

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

| 옵션 | 헤더 없음 | 헤더 있음 |
|---|---|---|
| add (2.21) | 추가 | 기존 값 유지 (변경 없음) |
| set (2.22) | 추가 | overwrite |
