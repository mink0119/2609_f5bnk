# 3.9 BackendTLSPolicy — wellKnownCACertificates: System

System CA 로 upstream TLS 검증. 사설 poc-backend-ca 는 System에 없으므로, 구현됐다면 match 실패여야 함.

## live 결과

- policy `status=` 없음. 컨트롤러 미처리
- pool :443 에 plain HTTP → 400 (System CA 검증 전에 upstream TLS 없음)
- iRule 없음

```bash
kubectl apply -f gw-backend-tls.yaml
kubectl delete -f gw-backend-tls.yaml
```
