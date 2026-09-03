# 3.2 Cross-namespace — Route to 다른 ns 백엔드

## 구성

```mermaid
flowchart LR
  C[Client] --> R["HTTPRoute ns=web"]
  R -->|ReferenceGrant| P1["Pool ns=web-backend"]
```

## 사전 준비

YAML이 Namespace `web-backend` + ReferenceGrant + Pool을 생성합니다.

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 다른 ns Pool로 전달

```bash
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- HTTPRoute ResolvedRefs=True

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
