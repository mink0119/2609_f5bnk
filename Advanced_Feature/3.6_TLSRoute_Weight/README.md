# 3.6 TLSRoute — weight

## 구성

```mermaid
flowchart LR
  C[Client TLS] --> GW[tls-gw Passthrough]
  GW -->|70| P1[coffee-pool]
  GW -->|30| P2[tea-pool]
```

## 적용

```bash
kubectl apply -f gw-tls-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 가중 분배 (백엔드가 TLS일 때)

```bash
for i in $(seq 1 20); do
  curl -k --resolve coffee.f5bnk.com:443:40.30.20.20 https://coffee.f5bnk.com/
  echo
done
```

**기대 응답**
- coffee 쪽이 더 많음 (약 70/30). 백엔드가 TLS가 아니면 핸드셰이크 실패

## 정리

```bash
kubectl delete -f gw-tls-route.yaml
```
