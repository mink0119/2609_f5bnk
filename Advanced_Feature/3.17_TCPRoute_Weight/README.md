# 3.17 TCPRoute — weight

TCPRoute 미지원. BNK native L4Route `backendRefs.weight` 70/30.

## live 결과

40회 TCP :80 → coffee 28 / tea 12.

```bash
kubectl apply -f gw-tcp-route.yaml
kubectl delete -f gw-tcp-route.yaml
```
