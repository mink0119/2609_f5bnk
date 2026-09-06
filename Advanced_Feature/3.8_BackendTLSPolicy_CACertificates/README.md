# 3.8 BackendTLSPolicy — caCertificateRefs

custom CA ConfigMap `backend-ca` 로 upstream TLS 검증.

## live 결과

- policy `coffee-backend-tls-ca` `status=` 없음. 컨트롤러 로그/이벤트 없음
- pool :443 에 plain HTTP → nginx 400
- CA 검증 자체를 실행하지 않음 (미구현)
- iRule 없음

```bash
kubectl apply -f gw-backend-tls.yaml
kubectl delete -f gw-backend-tls.yaml
```
