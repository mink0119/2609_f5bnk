# 3.19 UDPRoute — weight

## 구성

```mermaid
flowchart LR
  C[UDP] --> GW[udp-gw]
  GW -->|70| P1[coffee-pool]
  GW -->|30| P2[tea-pool]
```

## 적용

```bash
kubectl apply -f gw-udp-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. UDP 가중 분배

```bash
for i in $(seq 1 20); do
  echo -n "ping-$i" | nc -u -w 1 40.30.20.20 53
done
```

**기대 응답**
- coffee/tea 백엔드 캡처에서 수신 비율이 약 70/30
- 클라이언트 응답은 백엔드 UDP 구현에 따라 다름

## 정리

```bash
kubectl delete -f gw-udp-route.yaml
```
