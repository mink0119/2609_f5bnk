# 2.22 Request Header Modifier — remove

## 구성

```mermaid
flowchart LR
  C["X-Remove-Me: secret"] --> VIP[VIP]
  VIP -->|remove X-Remove-Me| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 지정 헤더 제거

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 -H 'X-Remove-Me: secret' http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- 백엔드 요청에 `X-Remove-Me` 가 없어야 함

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
