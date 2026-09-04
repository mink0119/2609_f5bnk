# 2.21 Request Header Modifier — add

## 구성

```mermaid
flowchart LR
  C["X-PoC-Add: client"] --> VIP[VIP]
  VIP -->|"add X-PoC-Add: added"| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 기존 값 유지 + 추가

```bash
curl -sS -D - -o /tmp/gw-body -H 'X-PoC-Add: client' --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- 백엔드에 기존 `client` 와 추가 `added` 가 함께 전달

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

add는 기존 헤더를 덮어쓰지 않고 값을 추가합니다.
