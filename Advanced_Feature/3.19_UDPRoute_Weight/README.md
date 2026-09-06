# 3.19 UDPRoute — weight

UDPRoute 미지원. BNK native L4Route weight 70/30, echo :9053.

## live 결과

40회 → coffee 27 / tea 13 (약 70/30).

```bash
kubectl apply -f gw-udp-route.yaml
kubectl delete -f gw-udp-route.yaml
```
