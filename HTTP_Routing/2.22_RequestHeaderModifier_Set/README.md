# 2.22 Request Header Modifier — set

## 구성

```mermaid
flowchart LR
  C["X-PoC-Set: client 또는 없음"] --> VIP[VIP]
  VIP -->|"set X-PoC-Set: overwritten"| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 있을 때 덮어씀

```bash
curl -sS -D - -o /tmp/gw-body -H 'X-PoC-Set: client' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- 백엔드 `X-PoC-Set` 는 `overwritten` 하나만

### 2. 없을 때 생성

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- 백엔드에 `X-PoC-Set: overwritten` 생성

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
