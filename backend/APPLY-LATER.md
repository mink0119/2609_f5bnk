# Apply after HTTP 2.35–2.45 finishes

이 파일은 초안입니다. HTTP 에이전트가 `http-gw` 를 쓰는 동안 SSH/nginx/kubectl apply 하지 마십시오.

## Backend (additive only)

1. `certs/` → `/etc/nginx/poc-certs/` + `conf.d/coffee-tls.conf` `tea-tls.conf` → `/etc/nginx/conf.d/`
2. `nginx -t` 후 `systemctl reload nginx` (`coffee.conf` / 기존 :80 vhost 덮어쓰기 금지)
3. `grpc/README.md` 대로 :50051 HelloService 3개
4. `udp/README.md` 대로 :9053 echo 2개 (`named` :53 건드리지 말 것)

## Cluster (one folder = one apply)

순서: 3.1 → 3.2 → 3.5 (HTTPS Terminate, F5 문서상 가능) → 3.10–3.14 (GRPCRoute) → 문서상 미지원 확인(3.3/3.4/3.6 TLSRoute, 3.7–3.9 BackendTLSPolicy, 3.15 sessionPersistence, 3.16–3.19 TCPRoute/UDPRoute).

매 항목 `kubectl delete -f` 후 다음.
