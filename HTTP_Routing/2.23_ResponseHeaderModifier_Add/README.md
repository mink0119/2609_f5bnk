# 2.23 Response Header Modifier — add

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP --> P1[coffee-pool]
  P1 --> VIP
  VIP -->|"add X-PoC-Res-Add: added"| C
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 응답 헤더 추가

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- 응답 헤더 `X-PoC-Res-Add: added`

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
