# Sheet facts — G/K Drive-verified 2026-09-05

Tab: `F5 Gateway API_KO(apigw v1.6)` (gid 1387085276)

CSV: https://docs.google.com/spreadsheets/d/1ls5qiYbk9c-eIZMMWZdChaatPgmK5Id4/export?format=csv&gid=1387085276

Column I was not changed. H left empty.

## Drive-saved (CSV confirmed)

| Item | G | K |
|---|---|---|
| 2.35 Service/port | O | *(empty — still pending short note)* |
| 2.36 ReferenceGrant | O | *(empty)* |
| 2.40 HTTPRetryCount | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
| 2.41 HTTPRetryBackoff | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
| 2.42 HTTPRetryCodes | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
| 2.43 SessionPersistence Cookie | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
| 2.44 SessionPersistence Header | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
| 2.45 rules[].name | O | *(empty)* |
| 3.2 CrossNamespace To | O | *(empty)* |
| 3.5 TLS Terminate | O | TLSRoute kind가 아니라 Gateway HTTPS listener + tls.mode Terminate + HTTPRoute + Secret. VIP cert=Secret, backend HTTP 200. 이전 BNK와 동일한 native terminate. |
| 3.10 GRPCRoute Method | O | *(empty)* |
| 3.14 GRPCRoute Weight | O | *(empty)* |
| 3.15 GRPC SessionPersistence | - | experimental 채널/필드라 이번 PoC에서 제외 (테스트 안 함) |
