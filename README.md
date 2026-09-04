# F5 Gateway API v1.6 PoC

F5 BNK에서 Gateway API v1.6 기능을 항목 단위로 검증하는 저장소입니다.

기능 번호·세부항목·테스트 시나리오는 이 파일이 아니라  
[`F5_Gateway_API_KO_apigw_v1.6.md`](F5_Gateway_API_KO_apigw_v1.6.md) 가 유일한 기준입니다.  
항목을 추가·수정할 때는 그 파일의 해당 번호를 먼저 읽고, 번호와 폴더가 어긋나지 않게 맞춥니다.

## 작업 방식

한 항목 = 한 폴더 = apply/delete 한 단위입니다.  
Gateway 이름이 항목마다 같으므로, 다음 항목으로 가기 전에 현재 YAML을 반드시 삭제합니다.

1. 명세에서 번호, 세부항목, 테스트 시나리오를 확인한다.
2. 폴더 `HTTP_Routing/` 또는 `Advanced_Feature/` 아래 `{번호}_{기능약칭}` 을 만든다.
3. YAML과 항목 `README.md` 를 작성한다. 기존 항목 폴더를 템플릿으로 쓴다.
4. `kubectl apply` → 클라이언트에서 검증 → `kubectl delete` 후 다음 항목으로 간다.

폴더명·내용은 명세와 1:1이어야 합니다. 이미지·이전 계획·추측으로 번호를 다시 매기지 않습니다.

## 고정 값

| 항목 | 값 |
|---|---|
| GatewayClass | `f5-bnk-gateway-class` |
| Namespace | `web` (크로스 네임스페이스 항목만 예외) |
| Gateway name | HTTP/gRPC → `http-gw`, TCP → `tcp-gw`, UDP → `udp-gw`, TLS → `tls-gw` |
| Listener | `bnk-listener` (포트가 둘이면 `bnk-listener-8080` 처럼 추가) |
| VIP | `40.30.20.20` (`addresses.type: IPAddress`) |
| Backend | `kind: Pool`, `group: k8s.f5net.com` |
| 기본 Host | `coffee.f5bnk.com` (hostname 항목이 아니면 이 값을 유지) |

Listener는 이름만 고정하고 protocol/port/kinds 는 항목에 맞게 바꿉니다.

### Backend Pool

외부 서버입니다. 새 member IP를 만들지 말고 아래 세 대만 사용합니다.

| Pool | Member | 기대 body |
|---|---|---|
| `coffee-pool` | `30.0.0.10:80` | `COFFEE SERVER - 30.0.0.10` |
| `tea-pool` | `30.0.0.11:80` | `TEA SERVER - 30.0.0.11` |
| `httpbin-pool` | `30.0.0.12:80` | `HTTPBIN CANARY SERVER - 30.0.0.12` |

### API 버전

이 클러스터 CRD 기준입니다.

| 리소스 | apiVersion |
|---|---|
| Gateway, HTTPRoute, GRPCRoute | `gateway.networking.k8s.io/v1` |
| TLSRoute, TCPRoute, UDPRoute | `gateway.networking.k8s.io/v1alpha2` |
| BackendTLSPolicy | `gateway.networking.k8s.io/v1alpha3` |
| ReferenceGrant | `gateway.networking.k8s.io/v1beta1` |
| Pool | `k8s.f5net.com/v1` |

## 파일 배치

```
F5_Gateway_API_KO_apigw_v1.6.md   # 기능 목록 (번호의 기준)
README.md                         # 이 파일 — 진행 규칙만
HTTP_Routing/                     # 2.x
  2.1_HTTProute/
    gw-http-route.yaml
    README.md
Advanced_Feature/                 # 3.x
  3.1_CrossNamespace_From/
    gw-http-route.yaml
    README.md
```

- 폴더명: `{번호}_{기능약칭}` — 번호는 명세와 동일
- YAML: HTTP는 `gw-http-route.yaml`, 그 외는 `gw-tls-route.yaml` / `gw-grpc-route.yaml` / `gw-tcp-route.yaml` / `gw-udp-route.yaml` / `gw-backend-tls.yaml`
- 한 폴더에 Gateway + Route + 그 항목에 필요한 Pool/Policy를 한 YAML에 넣습니다
- Route `parentRefs` 는 같은 파일의 Gateway `name` + `sectionName: bnk-listener`

## 항목 README

각 폴더 `README.md` 는 아래만 넣습니다. 명세 전체를 복사하지 않습니다.

1. 제목: 번호 + 세부항목
2. mermaid 구성도
3. `kubectl apply -f <yaml>`
4. 클라이언트 `curl` (또는 해당 프로토콜 명령) 과 **기대 응답**
5. `kubectl delete -f <yaml>`
6. 필요한 경우 GW API 제약만 한두 줄

적용·검증 명령은 VIP `40.30.20.20` 에 IP 터널로 도달하는 클라이언트에서 실행합니다.  
k8s 마스터에서 VIP로 직접 curl 하지 않습니다. Host는 `--resolve <host>:80:40.30.20.20` 을 씁니다.

## YAML을 쓸 때

기존 항목 YAML을 복사한 뒤, 명세의 해당 필드만 바꿉니다.

- `parentRefs.name` / `sectionName` 을 `web-http-gw` / `nginx` 로 쓰지 않습니다. 반드시 `http-gw`(또는 프로토콜별 Gateway) / `bnk-listener` 입니다.
- backend는 Service가 아니라 Pool입니다. Service/port 항목이라도 Pool 형식을 유지하고, 명세가 요구하는 `port` 필드만 추가합니다.
- hostname 검증이 목적인 항목이 아니면 `coffee.f5bnk.com` 하나만 둡니다.
- 한 항목에 비교 케이스가 있으면(Exact vs Wildcard, 301 vs 302 등) 같은 YAML에 HTTPRoute를 나누거나 rule을 나눕니다.
- TLS Terminate는 Secret `web-tls-cert`, BackendTLS CA는 ConfigMap `backend-ca` 를 전제로 적습니다. 없으면 README에 선행 조건을 적습니다.

## 검증 기준

- 성공: HTTP 200 + 위 Pool body, 또는 명세가 요구하는 status/Location/header
- 미매칭: 보통 404
- Redirect: statusCode와 Location. 303은 추종 시 GET, 307/308은 method/body 유지
- 미지원 필드: Route status `Accepted=False` / `UnsupportedValue` 를 확인하고 README에 적습니다
- ExternalAuth, gRPC, UDP, BackendTLS는 백엔드가 해당 프로토콜을 받을 수 있어야 합니다. 인프라가 없으면 YAML은 작성하고 README에 막힌 지점을 적습니다.
