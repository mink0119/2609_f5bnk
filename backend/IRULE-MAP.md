# iRule map (f5-bnk → this PoC)

Source: local checkout `/home/ncurity/bnk/bnk/f5-bnk` (BNK **2.1** Kakao lab).
GitHub `mink0119/f5-bnk` and `f5minions/f5-bnk` both 404 from this env; origin in that clone is `https://github.com/f5minions/f5-bnk.git`.

**Do not apply from this file.** Sibling owns `kubectl` for HTTP 2.35+.

## Attachment (every iRule in that repo)

Same two CRs, same namespace as the Gateway. No annotation, no ConfigMap, no CIS `VirtualServer`.

```yaml
apiVersion: k8s.f5net.com/v1
kind: F5BigCneIrule
metadata:
  name: irule-NAME
  namespace: web
spec:
  iRule: |
    when HTTP_REQUEST { ... }

---
apiVersion: gateway.k8s.f5net.com/v1alpha1
kind: BNKNetPolicy
metadata:
  name: netpolicy-NAME
  namespace: web
spec:
  extensionRefs:
    - kind: F5BigCneIrule
      name: irule-NAME
      group: k8s.f5net.com
  targetRefs:
    - kind: Gateway
      name: GATEWAY
      group: gateway.networking.k8s.io
      sectionName: LISTENER   # required in all their samples
```

BNK 2.3 docs still use this pair (`F5BigCneIrule` + `BNKNetPolicy`). Listener-scoped via `sectionName`.

**Scope limit:** iRule is Gateway/listener-wide. Path/`HTTP::method` branching is how they fake per-rule filters. There is **no** per-`backendRef` attach in the repo.

## Sheet convention (match CORS)

Native first. If CRD reject / `Accepted=False` / missing behavior:

| G (native) | H `iRule 필요` | K 비고 |
|---|---|---|
| x | O | why native failed + which f5-bnk iRule |

CORS native fail already seen here: HTTPRoute `filters[].type` enum is only `RequestHeaderModifier`, `ResponseHeaderModifier`, `RequestMirror`, `RequestRedirect`, `URLRewrite`, `ExtensionRef` — **`CORS` is rejected**.

---

## iRules that exist (8)

All are HTTP. All already-tested band **2.11–2.32** except the 2.37 analogue note.

| PoC # | Folder | f5-bnk file | Bypass | iRule (summary) | Remaining? |
|---|---|---|---|---|---|
| **2.30–2.32 CORS** | `HTTP_Routing/2.30_HTTPCORS_OriginsCredentials`, `2.31_HTTPCORS_MethodsHeaders`, `2.32_HTTPCORS_ExposeHeadersMaxAge` | `2.httproute/2.19_httproute-cors.yaml` (`irule-cors`) | Native `type: CORS` not in BNK HTTPRoute filter enum (they commented the filter out) | `HTTP_RESPONSE`: if no ACAO insert `Access-Control-Allow-Origin: app.kakao.com` + `Credentials: true`; else replace ACAO. **No OPTIONS preflight, no origin allowlist, no methods/headers/maxAge/exposeHeaders.** | Sheet convention only (already tested) |
| **2.11** HTTP→HTTPS | `2.11_HTTPRedirect_Scheme` | `2.httproute/2.2_httproute-redirect-http.yaml` | BNK 2.1: `RequestRedirect` not implemented; they still put the filter in YAML and overlay iRule | `HTTP_REQUEST` → `HTTP::respond 301 Location "https://[getfield [HTTP::host] \":\" 1][HTTP::uri]"` | already tested |
| **2.12 / 2.16 / 2.17** 302 + path | `2.12_HTTPRedirect_StatusCode`, `2.16_HTTPRedirect_ReplaceFullPath`, `2.17_HTTPRedirect_ReplacePrefixMatch` | `2.httproute/2.5_httproute-path-redirect.yaml` | 302 / path redirect not native | `/latte*` → 302 Location host+`string map /latte→/black` (prefix); `/coffee*` → 302 `/green/tea` (full) | already tested |
| **2.13** 303 PRG | `2.13_HTTPRedirect_StatusCode_303` | `2.httproute/2.4_httproute-post-redirect-get.yaml` | 303 not native | POST → `HTTP::respond 303 Location "http://host/black/tea"` | already tested |
| **2.14** 307/308 | `2.14_HTTPRedirect_StatusCode_307_308` | `2.httproute/2.3_httproute-method-preserve-redirect.yaml` | method-preserve redirect not native (YAML has 301; iRule is 307) | `/coffee*` → 307 Location `http://host` + map `/coffee`→`/tea` | already tested |
| **2.15** hostname/port redirect | `2.15_HTTPRedirect_HostnamePort` | (partial: 2.2 uses `[HTTP::host]`, no port rewrite) | — | no dedicated iRule | already tested |
| **2.18–2.20** URLRewrite | `2.18_HTTPURLRewrite_Hostname`, `2.19_…ReplaceFullPath`, `2.20_…ReplacePrefixMatch` | `2.httproute/2.8_httproute-rewrite.yaml` | Path + Host rewrite not native (YAML wrongly uses `RequestRedirect`; iRule is rewrite) | `/ip` + host `old.f5bnk.com` → `HTTP::uri` map `/ip`→`/headers`, `HTTP::host new.f5bnk.com`; `/user-agent` → uri `/headers` + same host | already tested |
| **2.21–2.26** header modifiers | `2.21_RequestHeaderModifier_*` … `2.26_ResponseHeaderModifier_Remove` | `2.httproute/2.9_httproute-request-response-modifier.yaml` | Request/Response header add/set/remove not native | REQ: `/headers` replace UA; `/coffee` remove `X-tea-id`; else insert Host. RESP: replace `X-Frame-Options`, remove `X-Content-Type-Options`, insert `X-XSS-Protection` | **2.37** closest analogue |
| **2.27** RequestMirror 100% | `2.27_HTTPRequestMirror` | `2.httproute/2.17_http-request-mirror.yaml` | No native `RequestMirror` in that lab | `HTTP::collect` + `HSL::open -proto TCP -pool f5-bnk-pool-spkpool-mirror-pool` + `HSL::send` payload. Needs extra `F5SPKPool`. Not a Gateway `backendRef` mirror; HSL side-copy. | **3.13** closest analogue only |
| **2.28** Mirror percent | `2.28_HTTPRequestMirror_Percent` | — | — | **no iRule in repo** | already tested |
| **2.29** weights | `2.29_HTTPTrafficSplitting` | `2.httproute/2.18_httproute-splitting.yaml` | native `backendRefs.weight` (90/10) | **no iRule** (weights worked native in 2.1) | already tested; 3.6/3.14/3.17/3.19 same |

### CORS re-apply sketch (sheet example)

```tcl
when HTTP_RESPONSE {
  if { !([HTTP::header exists "Access-Control-Allow-Origin"]) } {
    HTTP::header insert "Access-Control-Allow-Origin" "https://shop.f5bnk.com"
    HTTP::header insert "Access-Control-Allow-Credentials" "true"
  } else {
    HTTP::header replace "Access-Control-Allow-Origin" "https://shop.f5bnk.com"
    HTTP::header insert "Access-Control-Allow-Credentials" "true"
  }
}
```

K 비고 example: `네이티브 CORS 필터 CRD 거부(enum에 CORS 없음). f5-bnk 2.19 iRule은 응답 헤더 고정 삽입만. preflight/allowlist 미구현.`

---

## Remaining 2.35+ / 3.1–3.19 — only if repo has an analogue

| PoC # | Item | iRule in repo? | If native fails |
|---|---|---|---|
| 2.35 | BackendRef Service/port | **no iRule** | iRule cannot resolve Service/Pool |
| 2.36 | namespace / ReferenceGrant | **no iRule** | same |
| **2.37** | backendRef.filters | **header/rewrite/redirect iRules only** (2.9 / 2.8 / 2.2–2.5) | Listener-wide path-branch, **not** per-backendRef. 2.9 insert/set/remove is the CORS-style fallback for header filters. G=x H=O K=`backendRef.filters 미지원; 2.9 경로분기 header iRule` |
| 2.38–2.39 | timeouts request / backendRequest | **no iRule** | do not invent `after`/`HTTP::close` |
| 2.40–2.42 | retry codes/attempts/backoff | **no iRule** | — |
| 2.43–2.44 | sessionPersistence Cookie/Header | **no iRule** | no persist/cookie iRule in repo |
| 2.45 | rules[].name | **no iRule** | identity/schema only |
| 2.33–2.34 | ExternalAuth HTTP/gRPC | **no iRule** | already-tested band; no analogue |
| **3.1** | Cross-NS Selector | **no iRule** | repo uses native `from: Selector` (`3.Adcanced_Features/cross-ns-routing/3.1_cross-ns-routing.yaml`) |
| 3.2 | Cross-NS backendRef + ReferenceGrant | **no iRule** | — |
| **3.3–3.6** | TLSRoute SNI / Passthrough / Terminate / weight | **no iRule** | Passthrough workaround was **L4Route** + TCP listener (`3.Adcanced_Features/tls/3.3_tls_passthrough.yaml`), not iRule. Terminate was HTTPS listener + HTTPRoute (`3.2_tls_terminate.yaml`). **Do not call L4Route an iRule.** |
| **3.7–3.9** | BackendTLSPolicy | **no iRule** | README only has native `BackendTLSPolicy` YAML; no CR applied in tree |
| 3.10–3.12 | GRPC method / headers / modifiers | **no iRule** | 2.9 HTTP header iRule is not a gRPC metadata sample |
| **3.13** | GRPC RequestMirror | **no gRPC iRule** | HTTP 2.17 HSL mirror is the only mirror analogue; unproven on h2/gRPC |
| 3.14 | GRPC weight | **no iRule** | 2.18 native weights |
| **3.15** | GRPC sessionPersistence | **no iRule** | — |
| **3.16–3.19** | TCPRoute / UDPRoute / weights | **no iRule** | repo used **L4Route** (`tcproute/tcp-gw-route.yaml`, `udproute/udp-gw-route.yaml`), not iRule |

## Not in repo (do not invent)

Timeouts, retries, session persist, ExternalAuth, CORS preflight/allowlist, mirror percent, TLSRoute, BackendTLSPolicy, TCPRoute, UDPRoute, Selector, ReferenceGrant, gRPC sessionPersistence.
