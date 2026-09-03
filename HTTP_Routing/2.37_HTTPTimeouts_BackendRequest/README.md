# 2.37 HTTP Timeouts — backendRequest

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|request 10s / backendRequest 2s| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상 응답

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. backendRequest 2s

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/slow
```

**기대 응답**
- 백엔드 지연 > 2s 이면 timeout. 클라이언트 전체 대기는 10s를 넘지 않음

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
