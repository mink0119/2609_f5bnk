# 3.16 TCPRoute — listener / parentRef

두 TCP listener/Route로 port별 backend를 나눕니다.

## 구성

```mermaid
flowchart LR
  C80["TCP :80"] --> GW[tcp-gw]
  C8080["TCP :8080"] --> GW
  GW -->|bnk-listener :80| P1["coffee-pool 30.0.0.10"]
  GW -->|bnk-listener-8080 :8080| P2["tea-pool 30.0.0.11"]
```

## 적용

```bash
kubectl apply -f gw-tcp-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. port 80 → coffee

```bash
echo -e 'GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n' | nc -w 3 40.30.20.20 80
```

**기대 응답**
- TCP 연결 성공
- Body `COFFEE SERVER - 30.0.0.10` (또는 coffee 서버의 / 응답)
- Host/path 매칭 없음 (L4)

### 2. port 8080 → tea

```bash
echo -e 'GET / HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n' | nc -w 3 40.30.20.20 8080
```

**기대 응답**
- TCP 연결 성공
- Body `TEA SERVER - 30.0.0.11`
- 양방향 payload가 해당 backend로만 감

## 정리

```bash
kubectl delete -f gw-tcp-route.yaml
```

## 참고

TCPRoute는 L4입니다. hostname/path 매칭이 없습니다.
