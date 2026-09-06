# 3.18 UDPRoute — Listener

UDPRoute kind 미지원. BNK native: **protocol UDP + L4Route**.  
백엔드 echo 는 **:9053** (named 가 :53).

## live 결과

VIP :9053 echo → `COFFEE UDP - 30.0.0.10 ping`  
Gateway supportedKinds=`L4Route`, Accepted/Programmed=True.

```bash
kubectl apply -f gw-udp-route.yaml
# bash: exec 3<>/dev/udp/40.30.20.20/9053; printf ping >&3; cat <&3
kubectl delete -f gw-udp-route.yaml
```
