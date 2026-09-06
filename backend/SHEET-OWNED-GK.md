# Owned G/H/K (Find/Replace one cell). Do not touch column I.

Tab gid 1387085276. H stays empty. Drive write from this agent: **blocked** (browser tab MCP dropped). Source of truth: `RETEST-NOTES.md`.

Find the current K (or G) string, replace once (not 모두 바꾸기 when K is shared), wait 드라이브에 저장됨, CSV-verify.

| Item | G cell | G | K cell | Find (current) | Replace K |
|---|---|---|---|---|---|
| 2.38 | G41 | X (already) | K41 | `timeouts.request:5s Accepted=True 이나 /delay/8이 8.0s 200. 카탈로그에 timeout iRule 없음` | `timeouts.request:5s Accepted=True. /delay/8 → 200 in 8.01s (미적용). timeout iRule 없음` |
| 2.39 | G42 | X (already) | K42 | `backendRequest:2s Accepted=True 이나 /delay/4가 4.0s 200. backendRequest>request는 CRD CEL 거부. 카탈로그에 timeout iRule 없음` | `backendRequest:2s Accepted=True. /delay/5 → 200 in 5.01s (미적용). timeout iRule 없음` |
| 3.3 | G51 | x (keep) | K51 | first of three identical TLS K | `TLSRoute 미지원. HTTPS listener hostname+HTTPRoute는 Host로 coffee/tea 200. SNI 인증서는 항상 tea.crt(SNI 미적용). iRule 없음` |
| 3.4 | G52 | **O** | K52 | second identical TLS K | `TLSRoute/protocol TLS 미지원. BNK native는 TCP+L4Route Passthrough. VIP fingerprint=백엔드 coffee.crt, body COFFEE TLS, :80 timeout` |
| 3.6 | G54 | **O** | K54 | last identical TLS K | `TLSRoute 미지원. HTTPS+HTTPRoute weight 70/30. 40회 coffee 28 / tea 12` |
| 3.7 | G55 | x (keep) | K55 | first of three identical BackendTLS K | `CRD 있음. 컨트롤러 미처리(status/로그/이벤트 없음). HTTP·HTTPS 모두 pool :443에 plain HTTP→400. SAN 검증 전 단계. iRule 없음` |
| 3.8 | G56 | x (keep) | K56 | second BackendTLS K | `CRD 있음. policy status 없음. 컨트롤러 미처리. pool :443 plain HTTP→400. custom CA 미적용. iRule 없음` |
| 3.9 | G57 | x (keep) | K57 | last BackendTLS K | `CRD 있음. wellKnown=System status 없음. 컨트롤러 미처리. pool :443 plain HTTP→400. iRule 없음` |
| 3.11 | G59 | x (keep) | K59 | current unique K | `Accepted=True. grpcurl metadata env=canary/canary-foo/prod 백엔드 도달 확인. 전부 첫 rule(canary). gRPC header iRule 없음` |
| 3.12 | G60 | x (keep) | K60 | (optional keep) | `Accepted=True. 백엔드 md에 X-PoC-Add 없음. 응답/trailer에 X-PoC-Res-Add 없음. gRPC iRule 없음` |
| 3.13 | G61 | x (keep) | K61 | (optional keep) | `Accepted=True. 10 RPC client=coffee, tea:50051 미러 0. gRPC mirror iRule 없음` |
| 3.16 | G64 | **O** | K64 | first of two TCP K | `TCPRoute kind 미지원. BNK native L4Route. TCP :80→coffee 200, :8080→tea 200` |
| 3.17 | G65 | **O** | K65 | second TCP K | `TCPRoute 미지원. L4Route weight 70/30. 40회 coffee 28 / tea 12` |
| 3.18 | G66 | **O** | K66 | first of two UDP K | `UDPRoute kind 미지원. BNK native L4Route UDP :9053 → COFFEE UDP echo` |
| 3.19 | G67 | **O** | K67 | second UDP K | `UDPRoute 미지원. L4Route weight. 40회 coffee 27 / tea 13 (~70/30)` |

G cells that must flip `x` → `O` (do **not** 모두 바꾸기 on `x`): G52, G54, G64, G65, G66, G67.
Name-box each cell, type `O`, Enter. Do not paste G–K as a range.

Shared current K strings (replace **one occurrence** at a time, document order):

- 3.3/3.4/3.6: `protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음`
- 3.7/3.8/3.9: `BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용`
- 3.16/3.17: `Unsupported route kinds for protocol TCP: [TCPRoute]. supportedKinds=[]. BNK는 L4Route`
- 3.18/3.19: `UDP Gateway no valid listeners. supportedKinds=[]. UDPRoute parents 없음. BNK는 L4Route`
