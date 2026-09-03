# Gateway API v1.6 PoC — 기능 테스트 작성 계획

2.2~2.43, 3.1~3.19 YAML을 이 규칙으로 작성했습니다.  
`2.1_HTTProute`는 수정하지 않았습니다.

## 공통 규칙

테스트는 항목마다 YAML을 apply 하고, 다음 항목으로 갈 때 기존 YAML을 delete 합니다.

| 항목 | 고정 값 |
|---|---|
| GatewayClass | `f5-bnk-gateway-class` |
| Gateway name | 프로토콜별 고정. HTTP/gRPC → `http-gw`, TCP → `tcp-gw`, UDP → `udp-gw`, TLS → `tls-gw` |
| Namespace | `web` |
| Gateway address | `40.30.20.20` (IPAddress) |
| Listener | `bnk-listener` (프로토콜/포트만 항목에 맞게 변경) |
| Backend | `kind: Pool`, `group: k8s.f5net.com` |
| API | `gateway.networking.k8s.io/v1` (Gateway API v1.6) |

### Backend Pool (외부 클러스터)

2.1과 동일한 member를 재사용합니다. 항목에 백엔드가 더 필요하면 `30.0.0.10` ~ `30.0.0.12` 안에서만 나눕니다.

| Pool | Member |
|---|---|
| `coffee-pool` | `30.0.0.10:80` |
| `tea-pool` | `30.0.0.11:80` |
| `httpbin-pool` | `30.0.0.12:80` |

### 파일 배치

```
HTTP_Routing/
  2.1_HTTProute/                  # 기존 — 수정 안 함
  2.2_HTTPRouteMatch_Hostname/    # 이번 샘플
    gw-http-route.yaml
  2.3_...
Advanced_Feature/
  3.1_...
```

- 폴더명: `{번호}_{기능약칭}`
- YAML 파일명: `gw-http-route.yaml` (TLS/gRPC/TCP/UDP는 `gw-*-route.yaml`)
- 한 폴더 = 한 테스트 항목 = apply/delete 단위

---

## 폴더 / 항목 목록

번호와 세부항목은 첨부한 GW API v1.6 기능리스트 기준입니다.

### HTTP_Routing

| 폴더 | 검증 포인트 |
|---|---|
| `2.1_HTTProute` | 기본 HTTPRoute 전달 (기존) |
| `2.2_HTTPRouteMatch_Hostname` | hostname Exact / Wildcard (`*.example.com`). regex 없음 |
| `2.3_HTTPRouteMatch_PathExact` | path type Exact |
| `2.4_HTTPRouteMatch_PathPrefix` | path type PathPrefix |
| `2.5_HTTPRouteMatch_PathRegex` | path type RegularExpression |
| `2.6_HTTPRouteMatch_HeaderExact` | headers type Exact |
| `2.7_HTTPRouteMatch_HeaderRegex` | headers type RegularExpression |
| `2.8_HTTPRouteMatch_QueryExact` | queryParams type Exact |
| `2.9_HTTPRouteMatch_QueryRegex` | queryParams type RegularExpression |
| `2.10_HTTPRouteMatch_Method` | method (GET/POST 등) |
| `2.11_HTTPRedirect_Scheme` | RequestRedirect scheme (http → https) |
| `2.12_HTTPRedirect_StatusCode` | statusCode (301/302/307/308) |
| `2.13_HTTPRedirect_Hostname` | hostname 변경 |
| `2.14_HTTPRedirect_Port` | port 변경 |
| `2.15_HTTPRedirect_ReplaceFullPath` | path ReplaceFullPath |
| `2.16_HTTPRedirect_ReplacePrefixMatch` | path ReplacePrefixMatch |
| `2.17_HTTPURLRewrite_Hostname` | URLRewrite hostname |
| `2.18_HTTPURLRewrite_ReplaceFullPath` | URLRewrite path ReplaceFullPath |
| `2.19_HTTPURLRewrite_ReplacePrefixMatch` | URLRewrite path ReplacePrefixMatch |
| `2.20_RequestHeaderModifier_Add` | requestHeaderModifier add |
| `2.21_RequestHeaderModifier_Set` | requestHeaderModifier set |
| `2.22_RequestHeaderModifier_Remove` | requestHeaderModifier remove |
| `2.23_ResponseHeaderModifier_Add` | responseHeaderModifier add |
| `2.24_ResponseHeaderModifier_Set` | responseHeaderModifier set |
| `2.25_ResponseHeaderModifier_Remove` | responseHeaderModifier remove |
| `2.26_HTTPRequestMirror` | RequestMirror (보조 백엔드로 미러) |
| `2.27_HTTPTrafficSplitting` | backendRefs weight |
| `2.28_HTTPCORS_OriginsMethods` | allowOrigins / allowMethods |
| `2.29_HTTPCORS_Headers` | allowHeaders / exposeHeaders |
| `2.30_HTTPCORS_MaxAgeCredentials` | maxAge / allowCredentials |
| `2.31_HTTPExternalAuth_HTTP` | ExternalAuth HTTP |
| `2.32_HTTPExternalAuth_gRPC` | ExternalAuth gRPC |
| `2.33_HTTPBackendRef_ServicePort` | backendRef service/port (Pool 형식 유지) |
| `2.34_HTTPBackendRef_ReferenceGrant` | 크로스 네임스페이스 + ReferenceGrant |
| `2.35_HTTPBackendRef_Filters` | backendRef 내부 filters |
| `2.36_HTTPTimeouts_Request` | timeouts.request |
| `2.37_HTTPTimeouts_BackendRequest` | timeouts.backendRequest |
| `2.38_HTTPRetries_Codes` | retry codes |
| `2.39_HTTPRetries_Attempts` | retry attempts |
| `2.40_HTTPRetries_Backoff` | retry backoff |
| `2.41_SessionPersistence_Cookie` | sessionPersistence type Cookie |
| `2.42_SessionPersistence_Header` | sessionPersistence type Header |
| `2.43_HTTPRouteMeta` | Route 메타/annotation, status |

### Advanced_Feature

| 폴더 | 검증 포인트 |
|---|---|
| `3.1_CrossNamespace_From` | Gateway `allowedRoutes.namespaces.from` |
| `3.2_CrossNamespace_To` | Route → 다른 네임스페이스 백엔드 |
| `3.3_TLSRoute_HostnameSNI` | TLSRoute hostname (SNI) |
| `3.4_TLSRoute_Passthrough` | TLS mode Passthrough |
| `3.5_TLSRoute_Terminate` | TLS mode Terminate |
| `3.6_TLSRoute_Weight` | TLSRoute weight |
| `3.7_BackendTLSPolicy_TargetRef` | BackendTLSPolicy targetRef |
| `3.8_BackendTLSPolicy_CACertificates` | caCertificates |
| `3.9_BackendTLSPolicy_System` | System well-known CA |
| `3.10_GRPCRoute_Method` | gRPC method match |
| `3.11_GRPCRoute_Header` | gRPC header match |
| `3.12_GRPCRoute_Modifiers` | request/response modifier |
| `3.13_GRPCRoute_Mirror` | gRPC mirror |
| `3.14_GRPCRoute_Weight` | gRPC weight |
| `3.15_GRPCRoute_SessionPersistence` | gRPC session persistence |
| `3.16_TCPRoute_Listener` | TCPRoute listener/parentRef |
| `3.17_TCPRoute_Weight` | TCPRoute weight |
| `3.18_UDPRoute_Listener` | UDPRoute listener/parentRef |
| `3.19_UDPRoute_Weight` | UDPRoute weight |

시트 번호가 위와 한 칸 다르면 폴더명만 맞추면 됩니다. YAML 공통 규칙은 그대로입니다.

---

## 2.2 샘플 — hostname Exact / Wildcard

Gateway API v1.6 `HTTPRoute.spec.hostnames`:

- Exact: `coffee.f5bnk.com` — Host가 완전히 같을 때만 매칭
- Wildcard: `*.f5bnk.com` — 왼쪽 라벨 하나 이상 suffix 매칭. `foo.f5bnk.com`, `a.b.f5bnk.com`은 매칭. apex `f5bnk.com`은 매칭하지 않음
- regex 없음
- Exact와 Wildcard가 겹치면 Exact가 우선

이번 YAML:

| HTTPRoute | hostnames | Pool |
|---|---|---|
| `hostname-exact-route` | `coffee.f5bnk.com` | coffee-pool (`30.0.0.10`) |
| `hostname-wildcard-route` | `*.f5bnk.com` | tea-pool (`30.0.0.11`) |

path는 `PathPrefix: /`만 써서 hostname만 가르게 했습니다.

### 테스트 커맨드

```bash
# apply
kubectl apply -f HTTP_Routing/2.2_HTTPRouteMatch_Hostname/gw-http-route.yaml

# Exact — coffee
curl --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
# 기대: COFFEE SERVER - 30.0.0.10

# Wildcard — tea
curl --resolve shop.f5bnk.com:80:40.30.20.20 http://shop.f5bnk.com/
curl --resolve a.b.f5bnk.com:80:40.30.20.20 http://a.b.f5bnk.com/
# 기대: TEA SERVER - 30.0.0.11

# apex는 wildcard에 안 맞음
curl --resolve f5bnk.com:80:40.30.20.20 http://f5bnk.com/
# 기대: 매칭 없음 (보통 404)

# 다른 도메인
curl --resolve other.example.com:80:40.30.20.20 http://other.example.com/
# 기대: 매칭 없음 (보통 404)

# 다음 항목 전에 삭제
kubectl delete -f HTTP_Routing/2.2_HTTPRouteMatch_Hostname/gw-http-route.yaml
```

---

## 이후 진행

승인되면 2.3부터 같은 패턴으로 폴더 + YAML을 이어서 만들겠습니다.

확인해 주세요.

1. 폴더명/번호가 시트와 맞는지
2. 2.2 Exact + Wildcard를 한 YAML에 넣는 구성이 괜찮은지
3. Pool member `30.0.0.10/11/12`를 계속 써도 되는지
4. 2.2부터 이어서 전부 만들지, HTTP match(2.3–2.10)만 먼저 만들지
