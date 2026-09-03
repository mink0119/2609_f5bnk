# 2.34 HTTP BackendRef — ReferenceGrant

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP["Gateway/HTTPRoute ns=web"]
  VIP -->|ReferenceGrant| P1["Pool ns=web-backend 30.0.0.10"]
```

## 사전 준비

YAML이 `web-backend` Namespace를 만듭니다.

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 크로스 네임스페이스 백엔드

```bash
curl -sS -D - -o /tmp/gw-body  -H 'Host: coffee.f5bnk.com' http://40.30.20.20/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- `kubectl get httproute backendref-grant-route -n web` ResolvedRefs=True

### 2. Grant 상태

```bash
kubectl get referencegrant -n web-backend; kubectl get pool -n web-backend
```

**기대 응답**
- ReferenceGrant / Pool 이 web-backend 에 존재

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```
