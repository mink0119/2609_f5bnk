# 2.33 HTTP BackendRef — port

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|"backendRef port 80"| P1["coffee-pool 30.0.0.10:80"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. port 지정 전달

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- HTTPRoute Accepted / ResolvedRefs=True

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
