# 3.1 Cross-namespace — 다른 Namespace의 Route 연결 (from: All)

## 검증 목적

`web-route`의 HTTPRoute가 `web`의 Gateway listener에 연결되고 coffee backend로 요청을 전달하는지 검증합니다.
Gateway의 `allowedRoutes.namespaces.from: All`이 다른 Namespace의 Route 연결을 허용합니다.
Namespace 라벨이나 Selector는 사용하지 않습니다.

- Gateway: `web/http-gw`, VIP `40.30.20.20:80`
- HTTPRoute: `web-route/cross-ns-from-route`
- Pool: `web-route/coffee-pool` → `30.0.0.10:80`
- Route와 Pool은 같은 Namespace이므로 ReferenceGrant는 필요하지 않습니다.
- `parentRefs.namespace: web`은 Gateway의 Namespace입니다.
- `backendRefs.namespace`를 생략했으므로 Pool은 Route의 Namespace인 `web-route`에서 찾습니다.

실제 요청은 client → Gateway 설정을 처리하는 TMM → backend로 전달됩니다.
HTTPRoute는 별도의 패킷 중계 서버가 아니라 설정 객체입니다.

## 사전 확인

master에서 이 폴더로 이동합니다.

```bash
cd /root/bnk/web/poc/Advanced_Feature/3.1_CrossNamespace_From
kubectl get namespace web
kubectl get gatewayclass f5-bnk-gateway-class
kubectl get httproute -A
```

3.1과 3.2는 같은 Gateway·VIP·Host를 사용하므로 순차 시험합니다.
기존 시험 Route가 같은 listener의 `coffee.f5bnk.com` 요청을 처리하지 않도록 해당 시험의 정리 절차를 먼저 수행합니다.
200 응답만으로는 이번 Route가 처리했음을 판정할 수 없습니다.

## 1. All 허용 시험

master:

```bash
kubectl apply -f gw-http-route.yaml
kubectl get gateway http-gw -n web -o yaml
kubectl get httproute cross-ns-from-route -n web-route -o yaml
```

controller 반영 후 기대:
- Gateway listener의 `allowedRoutes.namespaces.from: All`
- 대상 parent의 Route `Accepted=True`, `ResolvedRefs=True`
- condition의 `observedGeneration`이 현재 객체의 `metadata.generation`과 일치
- Gateway `Programmed=True`

client `192.168.48.250`:

```bash
curl --noproxy '*' -i --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
```

기대: HTTP 200, Body에 `COFFEE SERVER - 30.0.0.10`.
이 항목은 다른 Namespace의 Route 연결 허용을 검사하며 client의 IP나 Namespace를 제한하는 시험이 아닙니다.


## 정리

시험용 Route·Pool·Gateway만 삭제합니다. Namespace는 다른 리소스가 있을 수 있으므로 삭제하지 않습니다.
아래 Gateway 삭제는 이 시험이 단독 사용 중일 때 수행합니다.

```bash
kubectl delete httproute cross-ns-from-route -n web-route --ignore-not-found
kubectl delete pool coffee-pool -n web-route --ignore-not-found
kubectl delete gateway http-gw -n web --ignore-not-found
```

## 지원 범위와 출처

BNK 2.3 공식 Gateway 문서는 `All`과 `Same`을 지원하고 `Selector`는 미지원으로 명시합니다.
이번 시험은 Selector 기능을 판정하지 않습니다. 

- [Gateway API v1.6.1 Gateway 정의](https://github.com/kubernetes-sigs/gateway-api/blob/v1.6.1/apis/v1/gateway_types.go)
- [Gateway API Cross-Namespace routing](https://gateway-api.sigs.k8s.io/guides/user-guides/multiple-ns/)
- [F5 BNK Gateway 지원 범위](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html)
