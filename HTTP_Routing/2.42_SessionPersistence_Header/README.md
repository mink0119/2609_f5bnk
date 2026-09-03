# 2.42 Session Persistence — Header

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|응답 X-Session-ID| C
  C -->|요청 X-Session-ID| VIP
  VIP -->|같은 백엔드| P1[coffee or tea]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 세션 헤더 확인

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- 응답에 `X-Session-ID` (구현이 헤더를 내려주는 경우)

### 2. 같은 헤더로 고정

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 -H 'X-Session-ID: <id>' http://coffee.f5bnk.com/
```

**기대 응답**
- 동일 `X-Session-ID` 로 10회가 한 백엔드로만 가야 함

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
