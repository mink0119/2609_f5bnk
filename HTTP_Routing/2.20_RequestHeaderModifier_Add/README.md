# 2.20 Request Header Modifier — add

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|"add X-PoC-Add: added"| P1["coffee-pool 30.0.0.10"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 요청은 200으로 전달

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 -H 'X-PoC-Add: client' http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- `add`는 기존 헤더를 유지하고 값을 추가. 백엔드에 `X-PoC-Add: added` 가 보여야 함

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

요청 헤더 변경은 응답에 안 보일 수 있습니다. 백엔드 액세스 로그 또는 echo 서버로 확인합니다.
