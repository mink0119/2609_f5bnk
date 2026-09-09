# 3.2 Cross-namespace — 다른 Namespace의 Pool 참조 (ReferenceGrant)

## 검증 목적

`web`의 HTTPRoute가 `web-backend`의 F5 Pool을 참조할 때 ReferenceGrant에 따라 허용·거절되는지 검증합니다.

- Gateway: `web/http-gw`, VIP `40.30.20.20:80`
- HTTPRoute: `web/cross-ns-to-route`
- Pool: `web-backend/coffee-pool` → `30.0.0.10:80`
- ReferenceGrant: `web-backend/allow-httproute-to-pool`

Gateway의 `allowedRoutes.namespaces.from: All`은 Route 연결 허용 설정입니다.
다른 Namespace의 backend 참조를 허용하는 설정은 ReferenceGrant입니다.
이 시험은 Gateway와 Route가 같은 `web`에 있으므로 from: Same도 연결 조건을 만족하지만, 제공 YAML은 All을 사용합니다.

`backendRefs.namespace: web-backend`는 Pool 객체를 찾을 Namespace입니다.
실제 외부 서버 30.0.0.10이 Kubernetes Namespace 안에 배치된다는 뜻은 아닙니다.

## ReferenceGrant 해석

- `metadata.namespace: web-backend`: 참조 대상 Pool이 있는 Namespace에 Grant를 생성합니다.
- `from.namespace: web`, `from.kind: HTTPRoute`: web에 있는 HTTPRoute의 참조를 허용합니다.
- `to.group: k8s.f5net.com`, `to.kind: Pool`, `to.name: coffee-pool`: 해당 F5 Pool 하나만 허용합니다.
- from에는 Route 이름을 제한하지 않으므로 web의 다른 HTTPRoute도 이 Grant의 허용 대상입니다.
- 이 시험은 표준 Service가 아닌 F5 Pool backend의 cross-namespace 참조를 검증합니다.

## 사전 확인

master:

```bash
cd /root/bnk/web/poc/Advanced_Feature/3.2_CrossNamespace_To
kubectl get namespace web
kubectl get gatewayclass f5-bnk-gateway-class
kubectl get httproute -A
kubectl get referencegrant -A -o yaml
```

3.1과 같은 Gateway·VIP·Host를 사용하므로 두 시험을 동시에 적용하지 않습니다.
기존 시험의 정리 절차를 수행하고, 같은 Host·Path를 처리하는 다른 Route가 없는지 확인합니다.
다른 ReferenceGrant가 같은 Pool 참조를 허용하면 아래 거절 시험이 성립하지 않습니다.
기존 Grant를 임의로 삭제하지 말고 해당 참조에 대한 다른 허용이 없는 시험 조건을 확보합니다.

## 1. ReferenceGrant 허용 시험

master:

```bash
kubectl apply -f gw-http-route.yaml
kubectl get referencegrant allow-httproute-to-pool -n web-backend -o yaml
kubectl get httproute cross-ns-to-route -n web -o yaml
kubectl get gateway http-gw -n web -o yaml
```

controller 반영 후 기대:
- 대상 parent의 Route `Accepted=True`, `ResolvedRefs=True`
- condition의 `observedGeneration`이 현재 객체의 `metadata.generation`과 일치
- Gateway `Programmed=True`

client `192.168.48.250`:

```bash
curl --noproxy '*' -i --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

기대: HTTP 200, Body에 `COFFEE SERVER - 30.0.0.10`.

## 정리

시험 리소스만 삭제하고 Namespace는 유지합니다.
아래 Gateway 삭제는 이 시험이 단독 사용 중일 때 수행합니다.

```bash
kubectl delete httproute cross-ns-to-route -n web --ignore-not-found
kubectl delete referencegrant allow-httproute-to-pool -n web-backend --ignore-not-found
kubectl delete pool coffee-pool -n web-backend --ignore-not-found
kubectl delete gateway http-gw -n web --ignore-not-found
```

## 출처

- [Gateway API ReferenceGrant](https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/)
- [Gateway API v1.6.1 ReferenceGrant 정의](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.1/apis/v1/referencegrant_types.go)
- [Gateway API v1.6.1 HTTPRoute 정의](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.1/apis/v1/httproute_types.go)

제공 YAML의 ReferenceGrant는 v1beta1을 유지합니다. 현재 클러스터에서는 v1과 v1beta1 모두 served=true로 확인했습니다.
