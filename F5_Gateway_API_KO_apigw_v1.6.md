# bnk:v2.3, gw api:v1.6

## 2.1

- 번호: 2.1
- 항목: HTTP Routing
- 중분류: HTTP Route
- 세부항목: HTTPRoute 기본 전달
- 설명: HTTP 타입 요청을 Service backendRef로 전달
  - hostname match, header match
- 테스트 시나리오(명세파일 등): HTTPRoute 생성 후 Host/Path가 일치하는 요청이 지정 Servicet로 전달되는지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/guides/user-guides/http-routing/

## 2.2

- 번호: 2.2
- 중분류: HTTP Route Match
- 세부항목: hostnames (Exact/Wildcard)
- 설명: Host 헤더를 정확 일치 또는 *.example.com 형태의 wildcard로 매칭
- 테스트 시나리오(명세파일 등): 정확 Host, 하위 도메인, 비일치 Host를 호출하여 Route 선택 결과 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.3

- 번호: 2.3
- 세부항목: path.type: Exact
- 설명: 대소문자를 구분하여 전체 경로가 정확히 일치하는 요청만 매칭
- 테스트 시나리오(명세파일 등): /api, /api/, /api/v1을 각각 호출하여 Exact 경로만 전달되는지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.4

- 번호: 2.4
- 세부항목: path.type: PathPrefix
- 설명: / 구분자 기준으로 경로 prefix가 일치하는 요청을 매칭
- 테스트 시나리오(명세파일 등): /api, /api/v1은 매칭되고 /apix는 매칭되지 않는지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.5

- 번호: 2.5
- 세부항목: path.type: RegularExpression
- 설명: 정규식으로 요청 경로를 매칭하며 문법은 구현체별 상이
- 테스트 시나리오(명세파일 등): 지원 정규식 문법과 우선순위를 확인하고 미지원 시 Accepted=False/UnsupportedValue 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.6

- 번호: 2.6
- 세부항목: headers.type: Exact
- 설명: 지정한 HTTP header name/value가 정확히 일치할 때 매칭
- 테스트 시나리오(명세파일 등): header 일치·불일치·미포함 요청으로 backend 분기 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.7

- 번호: 2.7
- 세부항목: headers.type: RegularExpression
- 설명: HTTP header value를 정규식으로 매칭
- 테스트 시나리오(명세파일 등): 구현체 지원 정규식과 미지원 값의 Route status 처리 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.8

- 번호: 2.8
- 세부항목: queryParams.type: Exact
- 설명: query parameter name/value가 정확히 일치할 때 매칭
- 테스트 시나리오(명세파일 등): 동일 path에 서로 다른 query parameter를 전송하여 backend 분기 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.9

- 번호: 2.9
- 세부항목: queryParams.type: RegularExpression
- 설명: query parameter value를 정규식으로 매칭
- 테스트 시나리오(명세파일 등): 지원 여부·정규식 문법·미지원 시 Route status 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 2.10

- 번호: 2.10
- 세부항목: method
- 설명: GET/HEAD/POST/PUT/DELETE/CONNECT/OPTIONS/TRACE/PATCH 요청 method로 매칭
- 테스트 시나리오(명세파일 등): 동일 Host/Path에 GET·POST 규칙을 구성하여 method별 backend 분기 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.11

- 번호: 2.11
- 중분류: HTTP Redirect
- 세부항목: HTTP-to-HTTPS redirect
- 설명: requestRedirect.scheme=https를 사용하여 HTTP 요청을 HTTPS로 redirect
- 테스트 시나리오(명세파일 등): HTTP 요청은 3xx/Location:https로 응답하고 HTTPS 요청은 backend로 전달되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.12

- 번호: 2.12
- 세부항목: statusCode: 301/302
- 설명: 영구/임시 redirect 상태코드와 Location 헤더 처리
- 테스트 시나리오(명세파일 등): 301 및 기본값 302 응답과 Location 구성요소 보존 여부 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.13

- 번호: 2.13
- 세부항목: statusCode: 303
- 설명: POST 요청 후 GET endpoint로 전환하는 POST-Redirect-GET 패턴
- 테스트 시나리오(명세파일 등): POST 요청에 303 응답 후 client가 Location을 GET으로 호출하는지 확인
- 공식 출처: Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.14

- 번호: 2.14
- 세부항목: statusCode: 307/308
- 설명: redirect 이후에도 원 요청 method와 body를 유지
- 테스트 시나리오(명세파일 등): POST/PUT 요청에 307·308 적용 후 method/body 보존 여부 확인
- 공식 출처: Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.15

- 번호: 2.15
- 세부항목: hostname / port
- 설명: redirect 대상 hostname 및 port를 변경
- 테스트 시나리오(명세파일 등): scheme·hostname·port 조합별 Location 헤더와 기본 port 생략 여부 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.16

- 번호: 2.16
- 세부항목: path: ReplaceFullPath
- 설명: 매칭 시 redirect 대상 전체 path를 지정 값으로 교체
- 테스트 시나리오(명세파일 등): /old/child 요청이 지정된 단일 path로 redirect되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.17

- 번호: 2.17
- 세부항목: path: ReplacePrefixMatch
- 설명: 매칭된 path prefix만 교체하고 나머지 suffix 유지
- 테스트 시나리오(명세파일 등): /old/child 요청이 /new/child로 redirect되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.18

- 번호: 2.18
- 중분류: HTTP URL Rewrite
- 세부항목: hostname
- 설명: client redirect 없이 upstream Host header를 지정 hostname으로 변경
- 테스트 시나리오(명세파일 등): client는 3xx를 받지 않고 backend가 변경된 Host를 수신하는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.19

- 번호: 2.19
- 세부항목: path: ReplaceFullPath
- 설명: backend 전달 전에 전체 request path를 교체
- 테스트 시나리오(명세파일 등): backend echo 결과에서 전체 path 교체 및 query string 보존 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.20

- 번호: 2.20
- 세부항목: path: ReplacePrefixMatch
- 설명: backend 전달 전에 매칭된 path prefix만 교체
- 테스트 시나리오(명세파일 등): backend echo 결과에서 suffix 유지 확인; RequestRedirect와 동시 사용 시 거부 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.21

- 번호: 2.21
- 중분류: Request Header Modifier
- 세부항목: add
- 설명: 기존 값을 유지하면서 request header 값을 추가
- 테스트 시나리오(명세파일 등): backend echo에서 기존 값과 추가 값이 함께 전달되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.22

- 번호: 2.22
- 세부항목: set
- 설명: request header를 지정 값으로 생성 또는 덮어쓰기
- 테스트 시나리오(명세파일 등): header 존재/미존재 조건 모두에서 단일 지정 값으로 전달되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.23

- 번호: 2.23
- 세부항목: remove
- 설명: 지정한 request header를 제거
- 테스트 시나리오(명세파일 등): 대소문자가 다른 동일 header까지 backend에서 제거되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.24

- 번호: 2.24
- 중분류: Response Header Modifier
- 세부항목: add
- 설명: 기존 값을 유지하면서 response header 값을 추가
- 테스트 시나리오(명세파일 등): client 응답에서 기존 값과 추가 값이 함께 존재하는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.25

- 번호: 2.25
- 세부항목: set
- 설명: response header를 지정 값으로 생성 또는 덮어쓰기
- 테스트 시나리오(명세파일 등): backend 원본 값을 Gateway가 지정 값으로 변경하는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.26

- 번호: 2.26
- 세부항목: remove
- 설명: 지정한 response header를 제거
- 테스트 시나리오(명세파일 등): backend가 생성한 대상 header가 client 응답에서 제거되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.27

- 번호: 2.27
- 중분류: HTTP Request Mirror
- 세부항목: backendRef (100%)
- 설명: 주 backend 응답만 client에 반환하고 요청 복사본을 mirror backend로 전달
- 테스트 시나리오(명세파일 등): 주 backend 응답은 유지되고 mirror backend는 요청을 수신하되 응답 영향이 없는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-request-mirroring/

## 2.28

- 번호: 2.28
- 세부항목: percent / fraction
- 설명: 요청의 일부만 percent 또는 numerator/denominator 비율로 미러링
- 테스트 시나리오(명세파일 등): 충분한 요청 표본으로 미러 수신 비율 확인; 둘 다 지정 시 fraction 우선 확인
- 공식 출처: Extended | v1.6 확인 항목 | https://gateway-api.sigs.k8s.io/geps/gep-3171/

## 2.29

- 번호: 2.29
- 중분류: HTTP Traffic Splitting
- 세부항목: backendRefs.weight
- 설명: 복수 backendRef의 상대 weight로 트래픽을 비율 분산
- 테스트 시나리오(명세파일 등): 예: 90/10과 1/1을 대량 호출하여 허용 오차 내 분산 및 weight=0 동작 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/traffic-splitting/

## 2.30

- 번호: 2.30
- 중분류: HTTP CORS
- 세부항목: allowOrigins / allowCredentials
- 설명: 허용 Origin과 credential 포함 여부를 설정
- 테스트 시나리오(명세파일 등): 허용·비허용 Origin 및 credential=true에서 wildcard 응답 제한 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.31

- 번호: 2.31
- 세부항목: allowMethods / allowHeaders
- 설명: preflight 요청에 허용할 method와 request header를 설정
- 테스트 시나리오(명세파일 등): OPTIONS preflight의 Access-Control-Allow-Methods/Headers 및 거부 동작 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.32

- 번호: 2.32
- 세부항목: exposeHeaders / maxAge
- 설명: client에 노출할 response header와 preflight cache 시간을 설정
- 테스트 시나리오(명세파일 등): Access-Control-Expose-Headers 및 Access-Control-Max-Age 값 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.33

- 번호: 2.33
- 중분류: HTTP External Auth
- 세부항목: protocol: HTTP
- 설명: 요청 전달 전 HTTP 인증/인가 서비스 호출
- 테스트 시나리오(명세파일 등): auth 200은 허용, 그 외 응답·연결 실패는 fail-close되는지 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 2.34

- 번호: 2.34
- 세부항목: protocol: GRPC
- 설명: Envoy ext_authz 호환 gRPC 인증/인가 서비스 호출
- 테스트 시나리오(명세파일 등): allow/deny/error 응답, metadata 및 header 전달·반환 동작 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 2.35

- 번호: 2.35
- 중분류: HTTP BackendRef
- 세부항목: Service / port
- 설명: backendRef의 group/kind/name/port로 대상 Service를 지정
- 테스트 시나리오(명세파일 등): 정상 Service/port 전달과 존재하지 않는 backend의 500·ResolvedRefs=False 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.36

- 번호: 2.36
- 세부항목: namespace / ReferenceGrant
- 설명: 다른 namespace의 Service를 ReferenceGrant를 통해 참조
- 테스트 시나리오(명세파일 등): Grant 미적용 시 RefNotPermitted, 적용 후 정상 전달 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/

## 2.37

- 번호: 2.37
- 세부항목: backendRef.filters
- 설명: 특정 backendRef로 전달할 때만 header/redirect/rewrite 등의 filter를 적용
- 테스트 시나리오(명세파일 등): 복수 backend 중 지정 backend에만 filter가 적용되는지와 지원 범위 확인
- 공식 출처: Filter별 Extended 또는 Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 2.38

- 번호: 2.38
- 중분류: HTTP Timeouts
- 세부항목: request
- 설명: client 요청 전체 처리 시간을 제한하며 0s는 timeout 비활성화
- 테스트 시나리오(명세파일 등): 지연 backend에서 설정 시간 전후 응답과 0s 동작 확인
- 공식 출처: Standard/Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-timeouts/

## 2.39

- 번호: 2.39
- 세부항목: backendRequest
- 설명: Gateway에서 backend로 보내는 개별 요청 시간을 제한
- 테스트 시나리오(명세파일 등): backendRequest가 request보다 클 때 스키마 거부 및 개별 요청 timeout 확인
- 공식 출처: Standard/Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-timeouts/

## 2.40

- 번호: 2.40
- 중분류: HTTP Retry
- 세부항목: codes
- 설명: 재시도할 HTTP 상태코드 지정; 500/502/503/504는 필수 지원 대상
- 테스트 시나리오(명세파일 등): 선택 상태코드만 재시도되는지 확인하고 중복 codes가 API에서 거부되는지 확인
- 공식 출처: Experimental/Extended | v1.6 validation | https://gateway-api.sigs.k8s.io/geps/gep-1731/

## 2.41

- 번호: 2.41
- 세부항목: attempts
- 설명: backend 요청의 최대 재시도 횟수 지정
- 테스트 시나리오(명세파일 등): 실패 후 성공 backend로 실제 호출 횟수 확인; attempts=0 스키마 거부 확인
- 공식 출처: Experimental/Extended | v1.6 validation | https://gateway-api.sigs.k8s.io/geps/gep-1731/

## 2.42

- 번호: 2.42
- 세부항목: backoff
- 설명: 재시도 간 최소 대기 시간 지정
- 테스트 시나리오(명세파일 등): 호출 timestamp로 최소 backoff와 request/backendRequest timeout 상호작용 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1731/

## 2.43

- 번호: 2.43
- 중분류: Session Persistence
- 세부항목: type: Cookie
- 설명: Gateway가 발급한 cookie로 동일 backend Pod에 세션 고정
- 테스트 시나리오(명세파일 등): Set-Cookie 수신 후 50회 이상 재호출하여 동일 Pod 유지 및 lifetime/absoluteTimeout 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/

## 2.44

- 번호: 2.44
- 세부항목: type: Header
- 설명: 지정 header 값을 이용하여 동일 backend Pod에 세션 고정
- 테스트 시나리오(명세파일 등): 동일 header 값의 backend 고정과 서로 다른 값의 독립 분산 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/

## 2.45

- 번호: 2.45
- 중분류: HTTP Route Rule
- 세부항목: rules[].name
- 설명: Route 내부 rule을 식별하는 고유 name 지정
- 테스트 시나리오(명세파일 등): 중복 name 스키마 거부와 sectionName 참조가 필요한 구현 기능에서 식별 가능 여부 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 3.1

- 번호: 3.1
- 항목: Advanced Features
- 중분류: Cross-Namespace Routing
- 세부항목: Route parentRef
- 설명: 다른 namespace의 Gateway listener에 Route를 연결
- 테스트 시나리오(명세파일 등): allowedRoutes가 허용할 때만 Route Accepted=True 및 트래픽 전달 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/cross-namespace-routing/

## 3.2

- 번호: 3.2
- 세부항목: Route backendRef
- 설명: 다른 namespace의 backend를 ReferenceGrant로 참조
- 테스트 시나리오(명세파일 등): ReferenceGrant 생성·삭제에 따라 ResolvedRefs와 전달 결과가 변경되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/

## 3.3

- 번호: 3.3
- 중분류: TLSRoute
- 세부항목: hostnames (SNI)
- 설명: TLS ClientHello의 SNI hostname으로 backend를 선택
- 테스트 시나리오(명세파일 등): 복수 SNI와 wildcard를 호출하여 올바른 backend 선택 및 미매칭 동작 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/

## 3.4

- 번호: 3.4
- 세부항목: mode: Passthrough
- 설명: Gateway가 TLS를 종료하지 않고 암호화 stream을 backend로 전달
- 테스트 시나리오(명세파일 등): backend가 인증서를 제공하고 Gateway에서 HTTP payload를 해석하지 않는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/

## 3.5

- 번호: 3.5
- 세부항목: mode: Terminate
- 설명: Gateway에서 TLS를 종료한 후 backend로 전달
- 테스트 시나리오(명세파일 등): Gateway 인증서 제공, 복호화 후 backend 전달 및 필요 시 BackendTLSPolicy 재암호화 확인
- 공식 출처: Extended | 기존 Terminate 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/tls/

## 3.6

- 번호: 3.6
- 세부항목: backendRefs.weight
- 설명: TLSRoute에서 복수 backend로 상대 weight 분산
- 테스트 시나리오(명세파일 등): 동일 SNI 연결을 충분히 반복하여 backend 연결 분포 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 3.7

- 번호: 3.7
- 중분류: BackendTLSPolicy
- 세부항목: hostname / subjectAltNames
- 설명: upstream TLS SNI와 서버 인증서 hostname/SAN 검증
- 테스트 시나리오(명세파일 등): 정상 hostname/SAN은 성공하고 불일치는 fail-close 및 policy status 오류 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/

## 3.8

- 번호: 3.8
- 세부항목: caCertificateRefs
- 설명: ConfigMap의 명시적 CA bundle로 upstream 서버 인증서 검증
- 테스트 시나리오(명세파일 등): 정상 CA, 잘못된 CA, ConfigMap 변경·삭제 시 재조정 결과 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/

## 3.9

- 번호: 3.9
- 세부항목: wellKnownCACertificates: System
- 설명: 구현체의 system trust store를 이용해 upstream 인증서 검증
- 테스트 시나리오(명세파일 등): 공인 CA backend 성공과 비신뢰 CA backend 실패 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/

## 3.10

- 번호: 3.10
- 중분류: GRPCRoute
- 세부항목: method.service / method.method
- 설명: gRPC service 및 method 이름으로 요청 분기
- 테스트 시나리오(명세파일 등): 서비스 전체 매칭과 특정 RPC method 매칭을 각각 호출하여 backend 분기 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/grpc-routing/

## 3.11

- 번호: 3.11
- 세부항목: headers (Exact/Regex)
- 설명: gRPC metadata header 값으로 요청 분기
- 테스트 시나리오(명세파일 등): 정확 일치와 구현체 정규식 지원 여부를 구분하여 backend 분기 확인
- 공식 출처: Core/Implementation-specific | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/grpc-routing/

## 3.12

- 번호: 3.12
- 세부항목: Request/ResponseHeaderModifier
- 설명: gRPC 요청·응답 metadata header 추가/수정/삭제
- 테스트 시나리오(명세파일 등): backend 및 client에서 add/set/remove 결과 확인
- 공식 출처: Core/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 3.13

- 번호: 3.13
- 세부항목: RequestMirror
- 설명: gRPC 요청을 mirror backend로 복제하고 mirror 응답은 무시
- 테스트 시나리오(명세파일 등): 주 backend 응답 유지, mirror 수신 및 percent/fraction 비율 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/geps/gep-3171/

## 3.14

- 번호: 3.14
- 세부항목: backendRefs.weight
- 설명: 복수 gRPC backendRef로 상대 weight 분산
- 테스트 시나리오(명세파일 등): 대량 RPC 호출로 분산 비율과 invalid backend의 UNAVAILABLE 비율 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 3.15

- 번호: 3.15
- 세부항목: sessionPersistence
- 설명: Cookie 또는 Header 기반으로 gRPC 세션을 동일 backend에 고정
- 테스트 시나리오(명세파일 등): 세션 token 재전송 시 동일 Pod 유지 여부 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/

## 3.16

- 번호: 3.16
- 중분류: TCPRoute
- 세부항목: listener / parentRef
- 설명: TCP listener port에 TCPRoute를 연결하여 raw TCP stream 전달
- 테스트 시나리오(명세파일 등): 두 listener/Route 구성 후 port별 backend 연결 및 양방향 payload 확인
- 공식 출처: v1.6 Standard/GA | 기존 v1.4 판단 유지 | https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.0

## 3.17

- 번호: 3.17
- 세부항목: backendRefs.weight
- 설명: 복수 TCP backendRef로 상대 weight 연결 분산
- 테스트 시나리오(명세파일 등): 반복 연결로 backend 선택 분포와 weight=0 동작 확인
- 공식 출처: v1.6 Standard/Core | https://gateway-api.sigs.k8s.io/guides/user-guides/tcp/

## 3.18

- 번호: 3.18
- 중분류: UDPRoute
- 세부항목: listener / parentRef
- 설명: UDP listener port에 UDPRoute를 연결하여 datagram 전달
- 테스트 시나리오(명세파일 등): 두 listener/Route 구성 후 port별 backend와 request/reply payload 확인
- 공식 출처: v1.6 Standard/GA | 기존 v1.4 판단 유지 | https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.0

## 3.19

- 번호: 3.19
- 세부항목: backendRefs.weight
- 설명: 복수 UDP backendRef로 상대 weight datagram 분산
- 테스트 시나리오(명세파일 등): 충분한 datagram 전송으로 backend 분포 및 응답 경로 확인
- 공식 출처: v1.6 Standard/Core | https://gateway-api.sigs.k8s.io/guides/user-guides/udp/
