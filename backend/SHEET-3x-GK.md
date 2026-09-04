# Paste-ready 3.x G/K (native-fail rows)

Tab: `F5 Gateway API_KO(apigw v1.6)` (gid 1387085276)

Do **not** paste a G–K range (that would overwrite H/I). Paste **G** then **K** per row.

Native-pass leave empty: 3.2 (row50), 3.5 (row53), 3.10 (row58), 3.14 (row62).
Already on Drive: 3.1 G49=`x` K49=`BNK 2.3: from=Selector는 Accepted되지만 미적용. unlabeled ns Route도 Accepted+전달(Selector가 All처럼 동작)`; 3.3 G51=`x`.

| 번호 | cell G | G | cell K | K |
|---|---|---|---|---|
| 3.3 | G51 | x | K51 | protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음 |
| 3.4 | G52 | x | K52 | protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음 |
| 3.6 | G54 | x | K54 | protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음 |
| 3.7 | G55 | x | K55 | BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용 |
| 3.8 | G56 | x | K56 | BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용 |
| 3.9 | G57 | x | K57 | BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용 |
| 3.11 | G59 | x | K59 | header match Accepted=True 이나 metadata 무시. 모든 RPC가 첫 rule(canary). gRPC iRule 없음 |
| 3.12 | G60 | x | K60 | HeaderModifier Accepted=True 이나 metadata 미적용. X-PoC-Add/Res-Add 없음. gRPC iRule 없음 |
| 3.13 | G61 | x | K61 | RequestMirror Accepted=True 이나 tea 미러 0건. client는 coffee만. gRPC iRule 없음 |
| 3.15 | G63 | x | K63 | unknown field spec.rules[0].sessionPersistence (CRD v1.6.1). GEP-1619 미포함 |
| 3.16 | G64 | x | K64 | Unsupported route kinds for protocol TCP: [TCPRoute]. supportedKinds=[]. BNK는 L4Route |
| 3.17 | G65 | x | K65 | Unsupported route kinds for protocol TCP: [TCPRoute]. supportedKinds=[]. BNK는 L4Route |
| 3.18 | G66 | x | K66 | UDP Gateway no valid listeners. supportedKinds=[]. UDPRoute parents 없음. BNK는 L4Route |
| 3.19 | G67 | x | K67 | UDP Gateway no valid listeners. supportedKinds=[]. UDPRoute parents 없음. BNK는 L4Route |

## Exact cells to paste

- **K51** — `protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음`
- **G52** — `x`
- **K52** — `protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음`
- **G54** — `x`
- **K54** — `protocol TLS 미지원 (UnsupportedProtocol). supportedKinds=[]. TLSRoute parents 없음`
- **G55** — `x`
- **K55** — `BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용`
- **G56** — `x`
- **K56** — `BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용`
- **G57** — `x`
- **K57** — `BackendTLSPolicy status 없음. Pool :443에 plain HTTP→400. SAN/CA 미적용`
- **G59** — `x`
- **K59** — `header match Accepted=True 이나 metadata 무시. 모든 RPC가 첫 rule(canary). gRPC iRule 없음`
- **G60** — `x`
- **K60** — `HeaderModifier Accepted=True 이나 metadata 미적용. X-PoC-Add/Res-Add 없음. gRPC iRule 없음`
- **G61** — `x`
- **K61** — `RequestMirror Accepted=True 이나 tea 미러 0건. client는 coffee만. gRPC iRule 없음`
- **G63** — `x`
- **K63** — `unknown field spec.rules[0].sessionPersistence (CRD v1.6.1). GEP-1619 미포함`
- **G64** — `x`
- **K64** — `Unsupported route kinds for protocol TCP: [TCPRoute]. supportedKinds=[]. BNK는 L4Route`
- **G65** — `x`
- **K65** — `Unsupported route kinds for protocol TCP: [TCPRoute]. supportedKinds=[]. BNK는 L4Route`
- **G66** — `x`
- **K66** — `UDP Gateway no valid listeners. supportedKinds=[]. UDPRoute parents 없음. BNK는 L4Route`
- **G67** — `x`
- **K67** — `UDP Gateway no valid listeners. supportedKinds=[]. UDPRoute parents 없음. BNK는 L4Route`

G51 already `x` on Drive — skip unless empty.
