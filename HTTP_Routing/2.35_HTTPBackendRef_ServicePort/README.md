# 2.35 HTTP BackendRef — Service / port

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|"group/kind/name/port"| P1["coffee-pool :80"]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상 port 전달

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`
- ResolvedRefs=True

### 2. 없는 backend

```bash
kubectl get httproute backendref-port-route -n web -o jsonpath='{.status.parents[0].conditions}' ; echo
```

**기대 응답**
- 존재하지 않는 name으로 바꾸면 5xx, ResolvedRefs=False

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## 참고

`gw-http-route.yaml` 은 외부 클러스터 Pool(`k8s.f5net.com`)을 Service 자리에 사용합니다.  
실제 Kubernetes Service 는 아래 v2.

## Service (v2)

클러스터 `web` Namespace에 nginx Pod 1개와 ClusterIP Service를 올리고, HTTPRoute `backendRefs`가 그 Service를 `group/kind/name/port`로 가리킵니다.  
`port: 80` 은 Service port입니다. Pod listen / `targetPort` 는 `8080`입니다.

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|"kind: Service port 80"| S["coffee-svc :80"]
  S -->|targetPort 8080| P["nginx Pod"]
```

Pool YAML과 같이 apply 하지 않습니다.

```bash
kubectl apply -f gw-http-route-v2.yaml
kubectl get deploy,svc coffee-svc -n web
kubectl get po -n web -l app=coffee-svc
kubectl get httproute backendref-port-route -n web
```

**기대 응답**
- Pod `READY 1/1`
- Service `coffee-svc` ClusterIP `:80` → `8080`
- HTTPRoute `ResolvedRefs=True`

### 1. Service / port 전달

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SVC - in-cluster`
- ResolvedRefs=True

### 2. 없는 backend

```bash
kubectl get httproute backendref-port-route -n web -o jsonpath='{.status.parents[0].conditions}' ; echo
```

**기대 응답**
- 존재하지 않는 name으로 바꾸면 5xx, ResolvedRefs=False

```bash
kubectl delete -f gw-http-route-v2.yaml
```

