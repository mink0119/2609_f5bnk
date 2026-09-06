# LIVE retest notes (owned rows)

Cluster: GatewayClass `f5-bnk-gateway-class`, VIP `40.30.20.20`.
Traffic: `kubectl exec -n f5-bnk-instance f5-tmm-6h6gx -c debug`.
Backend SSH `192.168.48.254` (delay/TLS/gRPC/UDP already live; `coffee.conf` not overwritten).
iRule: none attached. Catalog has no timeout / TLSRoute / BackendTLS / gRPC / TCPRoute / UDPRoute iRules.
Cluster left empty after tests.

Sheet G: `O` = Gateway API native pass. `O (F5 CRD)` = Gateway API kind 실패, F5 `L4Route` CRD로 기능 구현. `X`/`x` native fail. H empty unless catalog iRule used.

| Item | G | H | Object used |
|---|---|---|---|
| 2.38 | X | | HTTPRoute `timeouts.request` |
| 2.39 | X | | HTTPRoute `timeouts.backendRequest` |
| 3.3 | x | | HTTPS listener `hostname` + HTTPRoute (TLSRoute 미지원) |
| 3.4 | O (F5 CRD) | | TCP :443 + L4Route Passthrough |
| 3.6 | O | | HTTPS Terminate + HTTPRoute weight |
| 3.7–3.9 | x | | BackendTLSPolicy CRD only; controller ignore |
| 3.11–3.13 | x | | GRPCRoute Accepted but behavior missing |
| 3.16–3.19 | O (F5 CRD) | | TCP/UDP + L4Route |

---

## 2.38 timeouts.request (G41)

- Apply `HTTP_Routing/2.38_HTTPTimeouts_Request/gw-http-route.yaml` (`request: 5s`).
- HTTPRoute Accepted=True, ResolvedRefs=True. Gateway Programmed=True.
- `GET /` → 200 `COFFEE SERVER - 30.0.0.10` t=0.006s
- `GET /delay/2` → 200 `DELAYED 2.0s` t=2.01s
- `GET /delay/8` → 200 `DELAYED 8.0s` t=8.01s (**timeout not enforced**)
- Backend: `poc-delay.py` via nginx `/delay/` on 30.0.0.10.
- **G=X H=** (no timeout iRule) **K=** `timeouts.request:5s Accepted=True. /delay/8 → 200 in 8.01s (미적용). timeout iRule 없음`

## 2.39 timeouts.backendRequest (G42)

- Apply `2.39_*` (`request: 10s`, `backendRequest: 2s`). Accepted=True.
- `GET /` 200; `/delay/1` 200 t=1.01s; `/delay/5` 200 t=5.01s (**backendRequest not enforced**)
- **G=X H=** **K=** `backendRequest:2s Accepted=True. /delay/5 → 200 in 5.01s (미적용). timeout iRule 없음`

## 3.4 TLS Passthrough (G52) — FEATURE PASS

- Do **not** use kind TLSRoute / protocol TLS (UnsupportedProtocol).
- Applied TCP :443 + `L4Route` → coffee-pool :443 (`Advanced_Feature/3.4_TLSRoute_Passthrough/gw-tls-route.yaml`).
- L4Route Accepted=True, Gateway Programmed, supportedKinds=`L4Route`.
- openssl VIP:443 SNI coffee → CN=coffee.f5bnk.com issuer=poc-backend-ca
- sha256 fingerprint VIP == `/etc/nginx/poc-certs/coffee.crt` `F6:F6:27:30:...:55:10`
- curl https → 200 `COFFEE TLS - 30.0.0.10`
- HTTP :80 timeout (no terminate path)
- **G=O (F5 CRD) H=** **K=** `TLSRoute/protocol TLS 미지원. BNK native는 TCP+L4Route Passthrough. VIP fingerprint=백엔드 coffee.crt, body COFFEE TLS, :80 timeout`

## 3.3 TLS Hostname SNI (G51)

- TLSRoute/protocol TLS 미지원. Native try: two HTTPS listeners `hostname:` + Secrets (coffee.crt / tea.crt) + HTTPRoute hostnames → :80 pools.
- Gateway both listeners Accepted/Programmed. HTTPRoutes Accepted.
- Host routing: `https://coffee.f5bnk.com/` → `COFFEE SERVER - 30.0.0.10`; tea → `TEA SERVER - 30.0.0.11`
- SNI cert: coffee SNI, tea SNI, other.example.com **모두 CN=tea.f5bnk.com** (last-wins, SNI 미적용)
- SNI=coffee + Host=tea → TEA SERVER (Host 라우팅, SNI 아님)
- Spec is “ClientHello SNI selects backend”. That is not implemented. Host after terminate works.
- **G=x H=** **K=** `TLSRoute 미지원. HTTPS listener hostname+HTTPRoute는 Host로 coffee/tea 200. SNI 인증서는 항상 tea.crt(SNI 미적용). iRule 없음`

## 3.6 TLS Weight (G54) — FEATURE PASS

- HTTPS Terminate + HTTPRoute weight 70/30 to coffee/tea :80 (same as HTTP 2.29).
- Accepted=True. 40 HTTPS requests → coffee **28** / tea **12**.
- **G=O H=** **K=** `TLSRoute 미지원. HTTPS+HTTPRoute weight 70/30. 40회 coffee 28 / tea 12`

## 3.7 BackendTLSPolicy hostname/SAN (G55)

- CRD exists (`backendtlspolicies.gateway.networking.k8s.io` v1).
- Applied HTTP :80 + policy (Pool :443) **and** HTTPS Terminate + same policy (re-encrypt).
- Policy `status=` **None**. No events. `f5-cne-controller` logs: no BackendTLS string.
- Traffic both shapes: nginx `400 The plain HTTP request was sent to HTTPS port` (Gateway sent HTTP/1.1 to :443).
- 400 proves missing upstream TLS, but the fail evidence is **controller does not reconcile the policy**.
- SAN match vs mismatch cannot be evaluated.
- **G=x H=** **K=** `CRD 있음. 컨트롤러 미처리(status/로그/이벤트 없음). HTTP·HTTPS 모두 pool :443에 plain HTTP→400. SAN 검증 전 단계. iRule 없음`

## 3.8 caCertificateRefs (G56)

- policy `coffee-backend-tls-ca` status=None. NO_BACKENDTLS in controller.
- HTTP → :443 400. Custom CA never applied.
- **G=x H=** **K=** `CRD 있음. policy status 없음. 컨트롤러 미처리. pool :443 plain HTTP→400. custom CA 미적용. iRule 없음`

## 3.9 wellKnownCACertificates System (G57)

- `wellKnown=System`, status=None, same 400. System CA never evaluated.
- **G=x H=** **K=** `CRD 있음. wellKnown=System status 없음. 컨트롤러 미처리. pool :443 plain HTTP→400. iRule 없음`

## 3.11 GRPC headers (G59)

- GRPCRoute Accepted=True. Metadata **was sent** (backend log `env: canary|canary-foo|prod`).
- All four cases returned `CANARY GRPC - 30.0.0.12` (first rule). Not a client-omitted-metadata bug.
- No gRPC header iRule in catalog.
- **G=x H=** **K=** `Accepted=True. grpcurl metadata env=canary/canary-foo/prod 백엔드 도달 확인. 전부 첫 rule(canary). gRPC header iRule 없음`

## 3.12 GRPC modifiers (G60)

- Accepted=True. Primary RPC coffee 200.
- Backend md only `user-agent`. No `x-poc-add`. grpcurl -vv: no `X-PoC-Res-Add` in headers/trailers.
- HTTP header iRules are listener-wide HTTP; not used (would not inject gRPC metadata).
- **G=x H=** **K=** `Accepted=True. 백엔드 md에 X-PoC-Add 없음. 응답/trailer에 X-PoC-Res-Add 없음. gRPC iRule 없음`

## 3.13 GRPC mirror (G61)

- Accepted=True. 10 RPC all `COFFEE GRPC`. tea journal SayHello **+0**, coffee **+10**.
- HTTP HSL mirror iRule exists but unproven on h2/gRPC; not attached.
- **G=x H=** **K=** `Accepted=True. 10 RPC client=coffee, tea:50051 미러 0. gRPC mirror iRule 없음`

## 3.16 TCP listener (G64) — FEATURE PASS

- TCPRoute kind rejected previously. Native: protocol TCP + L4Route.
- :80 → `COFFEE SERVER - 30.0.0.10`; :8080 → `TEA SERVER - 30.0.0.11`
- supportedKinds=`L4Route`, Accepted/Programmed=True.
- **G=O (F5 CRD) H=** **K=** `TCPRoute kind 미지원. BNK native L4Route. TCP :80→coffee 200, :8080→tea 200`

## 3.17 TCP weight (G65) — FEATURE PASS

- L4Route weight 70/30. 40 TCP hits → coffee **28** / tea **12**.
- **G=O (F5 CRD) H=** **K=** `TCPRoute 미지원. L4Route weight 70/30. 40회 coffee 28 / tea 12`

## 3.18 UDP listener (G66) — FEATURE PASS

- UDP :9053 + L4Route → coffee echo. `COFFEE UDP - 30.0.0.10 ping`
- **G=O (F5 CRD) H=** **K=** `UDPRoute kind 미지원. BNK native L4Route UDP :9053 → COFFEE UDP echo`

## 3.19 UDP weight (G67) — FEATURE PASS

- L4Route weight. 40 UDP → coffee **27** / tea **13** (~70/30).
- **G=O (F5 CRD) H=** **K=** `UDPRoute 미지원. L4Route weight. 40회 coffee 27 / tea 13 (~70/30)`

## 3.1

Not retested. Existing G=x (Selector acts like All) believed correct.

## Not owned / not tested

2.35/2.36/2.45/3.2/3.5/3.10/3.14/2.40–2.44/3.15 — other agent.
