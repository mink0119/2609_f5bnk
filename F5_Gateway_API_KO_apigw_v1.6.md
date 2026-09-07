# bnk:v2.3, gw api:v1.6

## 2.1

- 번호: 2.1
- 항목: HTTP Routing
- 중분류: HTTP Route
- 세부항목: HTTPRoute 기본 전달
- 설명: HTTP 타입 요청을 Service backendRef로 전달
  - hostname match, header match
- F5 지원: O
- 테스트 시나리오(명세파일 등): Host/Path 일치 시 지정 backend 전달, 미매칭 경로는 404, header match 시 canary backend 분기 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/guides/user-guides/http-routing/

## 2.2

- 번호: 2.2
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: hostnames (Exact/Wildcard)
- 설명: Host 헤더를 정확 일치 또는 *.example.com 형태의 wildcard로 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): Exact Host·wildcard 하위 도메인 매칭과 Exact 우선, apex 및 다른 도메인은 404인지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/
- 특이사항: policy 설정을 할 때 path 별로 pool 분기하는 설정을 어떻게 확인하는지 모르겠음. 명령어에 없는 듯 하다.
  - virtual server 에도 default pool 만 있으며, configview pool 에 다른 멤버들이 있는데 해당 멤버들이 virtual server 에 매핑된 정보도 없음 경로도 안 나옴..

## 2.3

- 번호: 2.3
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: path.type: Exact
- 설명: 대소문자를 구분하여 전체 경로가 정확히 일치하는 요청만 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): Exact 경로만 전달되고 prefix 확장·루트는 404인지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.4

- 번호: 2.4
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: path.type: PathPrefix
- 설명: / 구분자 기준으로 경로 prefix가 일치하는 요청을 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): 지정 prefix와 하위 경로는 매칭되고 다른 prefix는 404인지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.5

- 번호: 2.5
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: path.type: RegularExpression
- 설명: 정규식으로 요청 경로를 매칭하며 문법은 구현체별 상이
- F5 지원: X
- 테스트 시나리오(명세파일 등): regex 매칭 경로는 지정 backend, 불일치·루트는 default backend로 가는지 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/
- 특이사항: regex 기반 정책 적용이 안 되는 듯 - policy 확인이 안 되니 제대로 적용된지 설정 볼 방법이 없으며, LB 자체 기능은 확인 함.

## 2.6

- 번호: 2.6
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: headers.type: Exact
- 설명: 지정한 HTTP header name/value가 정확히 일치할 때 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): header 일치 시 canary backend, 미포함·값 불일치는 default backend인지 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.7

- 번호: 2.7
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: headers.type: RegularExpression
- 설명: HTTP header value를 정규식으로 매칭
- F5 지원: X
- 테스트 시나리오(명세파일 등): header regex 매칭 시 canary backend, 부분 문자열·미포함은 default backend인지 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.8

- 번호: 2.8
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: queryParams.type: Exact
- 설명: query parameter name/value가 정확히 일치할 때 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): 동일 path에서 query 일치 시 canary backend, 없음·불일치는 default backend인지 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.9

- 번호: 2.9
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: queryParams.type: RegularExpression
- 설명: query parameter value를 정규식으로 매칭
- F5 지원: X
- 테스트 시나리오(명세파일 등): query regex 매칭 시 지정 backend, 불일치·없음은 default backend인지 확인
- 공식 출처: Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 2.10

- 번호: 2.10
- 항목: HTTP Routing
- 중분류: HTTP Route Match
- 세부항목: method
- 설명: GET/HEAD/POST/PUT/DELETE/CONNECT/OPTIONS/TRACE/PATCH 요청 method로 매칭
- F5 지원: O
- 테스트 시나리오(명세파일 등): GET·POST method별 backend 분기, 미지정 method는 404인지 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.11

- 번호: 2.11
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: HTTP-to-HTTPS redirect
- 설명: requestRedirect.scheme=https를 사용하여 HTTP 요청을 HTTPS로 redirect
- F5 지원: O
- 테스트 시나리오(명세파일 등): HTTP 요청이 301과 Location https로 redirect되고 backend로 전달되지 않는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/
- 특이사항: redirect 마찬가지로 policy 나 이런 설정들 없으며, 설정 확인 불가 하지만 기능은 정상 동작 ( 이전에는 iRule 이였으나 개선 됨. )

## 2.12

- 번호: 2.12
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: statusCode: 301/302
- 설명: 영구/임시 redirect 상태코드와 Location 헤더 처리
- F5 지원: O
- 테스트 시나리오(명세파일 등): 302 응답과 Location hostname 변경 여부 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.13

- 번호: 2.13
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: statusCode: 303
- 설명: POST 요청 후 GET endpoint로 전환하는 POST-Redirect-GET 패턴
- F5 지원: O
- 테스트 시나리오(명세파일 등): POST에 303/Location 응답 후, 추종 시 method가 GET으로 바뀌고 body는 전달되지 않는지 확인
- 공식 출처: Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.14

- 번호: 2.14
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: statusCode: 307/308
- 설명: redirect 이후에도 원 요청 method와 body를 유지
- F5 지원: O
- 테스트 시나리오(명세파일 등): POST 307·PUT 308 추종 후에도 원 method와 body가 유지되는지 확인
- 공식 출처: Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.15

- 번호: 2.15
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: hostname / port
- 설명: redirect 대상 hostname 및 port를 변경
- F5 지원: O
- 테스트 시나리오(명세파일 등): hostname만, port만, scheme·hostname·port 조합별 Location 헤더와 기본 port 생략 여부 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.16

- 번호: 2.16
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: path: ReplaceFullPath
- 설명: 매칭 시 redirect 대상 전체 path를 지정 값으로 교체
- F5 지원: O
- 테스트 시나리오(명세파일 등): 하위 경로 요청이 suffix 없이 지정 path로 redirect되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.17

- 번호: 2.17
- 항목: HTTP Routing
- 중분류: HTTP Redirect
- 세부항목: path: ReplacePrefixMatch
- 설명: 매칭된 path prefix만 교체하고 나머지 suffix 유지
- F5 지원: O
- 테스트 시나리오(명세파일 등): 매칭 prefix만 교체되고 나머지 suffix는 유지되는지 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.18

- 번호: 2.18
- 항목: HTTP Routing
- 중분류: HTTP URL Rewrite
- 세부항목: hostname
- 설명: client redirect 없이 upstream Host header를 지정 hostname으로 변경
- F5 지원: O
- 테스트 시나리오(명세파일 등): client는 3xx 없이 원래 backend 응답을 받고, upstream Host만 변경되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.19

- 번호: 2.19
- 항목: HTTP Routing
- 중분류: HTTP URL Rewrite
- 세부항목: path: ReplaceFullPath
- 설명: backend 전달 전에 전체 request path를 교체
- F5 지원: O
- 테스트 시나리오(명세파일 등): client는 3xx 없이 200을 받고, backend에 전달되는 전체 path가 지정 값으로 교체되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.20

- 번호: 2.20
- 항목: HTTP Routing
- 중분류: HTTP URL Rewrite
- 세부항목: path: ReplacePrefixMatch
- 설명: backend 전달 전에 매칭된 path prefix만 교체
- F5 지원: O
- 테스트 시나리오(명세파일 등): client는 3xx 없이 200을 받고, 매칭 prefix만 교체되어 suffix가 유지되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-redirect-rewrite/

## 2.21

- 번호: 2.21
- 항목: HTTP Routing
- 중분류: Request Header Modifier
- 세부항목: add
- 설명: 기존 값을 유지하면서 request header 값을 추가
- F5 지원: ?
- 테스트 시나리오(명세파일 등): 요청에 대상 header가 없을 때만 추가되고, 이미 있으면 기존 값이 유지되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/
- 특이사항: 공식문서는 기존에 동일한 헤더가 존재하면 append 하는 것처럼 나와 있는데 기존 헤더가 있다면 append 한다고 되어 있는데 해당 기능 미동작

## 2.22

- 번호: 2.22
- 항목: HTTP Routing
- 중분류: Request Header Modifier
- 세부항목: set
- 설명: request header를 지정 값으로 생성 또는 덮어쓰기
- F5 지원: O
- 테스트 시나리오(명세파일 등): header가 있으면 지정 값으로 덮어쓰고, 없으면 생성되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.23

- 번호: 2.23
- 항목: HTTP Routing
- 중분류: Request Header Modifier
- 세부항목: remove
- 설명: 지정한 request header를 제거
- F5 지원: O
- 테스트 시나리오(명세파일 등): 지정 request header 제거와, 대소문자가 다른 동일 header 제거 여부 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.24

- 번호: 2.24
- 항목: HTTP Routing
- 중분류: Response Header Modifier
- 세부항목: add
- 설명: 기존 값을 유지하면서 response header 값을 추가
- F5 지원: O
- 테스트 시나리오(명세파일 등): client 응답에 지정 header가 추가되고 백엔드 원본 header는 유지되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.25

- 번호: 2.25
- 항목: HTTP Routing
- 중분류: Response Header Modifier
- 세부항목: set
- 설명: response header를 지정 값으로 생성 또는 덮어쓰기
- F5 지원: O
- 테스트 시나리오(명세파일 등): 백엔드 원본 Server 값이 Gateway 지정 값으로 덮어쓰이는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.26

- 번호: 2.26
- 항목: HTTP Routing
- 중분류: Response Header Modifier
- 세부항목: remove
- 설명: 지정한 response header를 제거
- F5 지원: O
- 테스트 시나리오(명세파일 등): 백엔드가 생성한 Server header가 client 응답에서 제거되는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-header-modifier/

## 2.27

- 번호: 2.27
- 항목: HTTP Routing
- 중분류: HTTP Request Mirror
- 세부항목: backendRef (100%)
- 설명: 주 backend 응답만 client에 반환하고 요청 복사본을 mirror backend로 전달
- F5 지원: X
- 테스트 시나리오(명세파일 등): client는 primary backend 응답만 수신하고, mirror backend는 동일 요청을 받되 응답에는 영향이 없는지 확인
- 공식 출처: Extended | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-request-mirroring/

## 2.28

- 번호: 2.28
- 항목: HTTP Routing
- 중분류: HTTP Request Mirror
- 세부항목: percent / fraction
- 설명: 요청의 일부만 percent 또는 numerator/denominator 비율로 미러링
- F5 지원: X
- 테스트 시나리오(명세파일 등): client 응답은 항상 primary이고, mirror 수신 비율이 percent/fraction과 맞는지 확인
- 공식 출처: Extended | v1.6 확인 항목 | https://gateway-api.sigs.k8s.io/geps/gep-3171/

## 2.29

- 번호: 2.29
- 항목: HTTP Routing
- 중분류: HTTP Traffic Splitting
- 세부항목: backendRefs.weight
- 설명: 복수 backendRef의 상대 weight로 트래픽을 비율 분산
- F5 지원: O
- 테스트 시나리오(명세파일 등): 90/10·1/1 weight 분산 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/traffic-splitting/
- 특이사항: weight 0은 bnk 에서는 1로 표시 됨. 0은 미지원인 듯 함.

## 2.30

- 번호: 2.30
- 항목: HTTP Routing
- 중분류: HTTP CORS
- 세부항목: allowOrigins / allowCredentials
- 설명: 허용 Origin과 credential 포함 여부를 설정
- F5 지원: X
- 테스트 시나리오(명세파일 등): Exact Origin+credentials true에서 Origin echo 및 Credentials true·ACAO `*` 금지, 비허용 Origin은 요청 전달하되 ACAO 미설정, allowOrigins `*` + credentials false에서 ACAO(`*` 또는 echo)와 Credentials 헤더 생략, hostname wildcard `https://*.host`의 한 라벨·복수 라벨 echo와 비매칭 Origin ACAO 없음 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.31

- 번호: 2.31
- 항목: HTTP Routing
- 중분류: HTTP CORS
- 세부항목: allowMethods / allowHeaders
- 설명: preflight 요청에 허용할 method와 request header를 설정
- F5 지원: X
- 테스트 시나리오(명세파일 등): OPTIONS preflight의 Allow-Methods/Allow-Headers가 설정 목록과 일치하는지, 목록에 없는 method·header는 Allow 목록에 없고 요청 자체는 403으로 막지 않는지 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.32

- 번호: 2.32
- 항목: HTTP Routing
- 중분류: HTTP CORS
- 세부항목: exposeHeaders / maxAge
- 설명: client에 노출할 response header와 preflight cache 시간을 설정
- F5 지원: X
- 테스트 시나리오(명세파일 등): OPTIONS preflight의 Max-Age가 설정 초인지, 실제 GET의 Expose-Headers가 설정 목록과 일치하고 Max-Age는 없는지 확인
- 공식 출처: Standard/Extended | v1.6 반영 | https://gateway-api.sigs.k8s.io/guides/user-guides/http-cors/

## 2.33

- 번호: 2.33
- 항목: HTTP Routing
- 중분류: HTTP External Auth
- 세부항목: protocol: HTTP
- 설명: 요청 전달 전 HTTP 인증/인가 서비스 호출
- F5 지원: -
- 테스트 시나리오(명세파일 등): auth 200이면 backend 전달, 그 외 응답·연결 실패는 fail-close되는지 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- 특이사항: support 는 extended 지만 gateway api crd 가 experimental 이여서 해당 항목 제외

## 2.34

- 번호: 2.34
- 항목: HTTP Routing
- 중분류: HTTP External Auth
- 세부항목: protocol: GRPC
- 설명: Envoy ext_authz 호환 gRPC 인증/인가 서비스 호출
- F5 지원: -
- 테스트 시나리오(명세파일 등): allow면 backend 전달, deny/error/프로토콜 불일치는 fail-close되는지 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- 특이사항: support 는 extended 지만 gateway api crd 가 experimental 이여서 해당 항목 제외

## 2.35

- 번호: 2.35
- 항목: HTTP Routing
- 중분류: HTTP BackendRef
- 세부항목: Service / port
- 설명: backendRef의 group/kind/name/port로 대상 Service를 지정
- F5 지원: O
- 테스트 시나리오(명세파일 등): 정상 Service/port 전달과 ResolvedRefs=True, 없는 backend의 5xx·ResolvedRefs=False 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 2.36

- 번호: 2.36
- 항목: HTTP Routing
- 중분류: HTTP BackendRef
- 세부항목: namespace / ReferenceGrant
- 설명: 다른 namespace의 Service를 ReferenceGrant를 통해 참조
- F5 지원: O
- 테스트 시나리오(명세파일 등): ReferenceGrant 적용 후 전달, 삭제 시 RefNotPermitted 및 트래픽 실패 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/

## 2.37

- 번호: 2.37
- 항목: HTTP Routing
- 중분류: HTTP BackendRef
- 세부항목: backendRef.filters
- 설명: 특정 backendRef로 전달할 때만 header/redirect/rewrite 등의 filter를 적용
- F5 지원: X
- iRule 필요: O
- 테스트 시나리오(명세파일 등): 복수 backend 중 지정 backend로 간 요청에만 filter header가 적용되는지 확인
- 공식 출처: Filter별 Extended 또는 Implementation-specific | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- 특이사항: backendRef.filters 미지원; 2.9 경로분기 header iRule

## 2.38

- 번호: 2.38
- 항목: HTTP Routing
- 중분류: HTTP Timeouts
- 세부항목: request
- 설명: client 요청 전체 처리 시간을 제한하며 0s는 timeout 비활성화
- F5 지원: X
- 테스트 시나리오(명세파일 등): 제한 시간 내 정상 응답, 초과 시 timeout, 0s는 timeout 비활성화인지 확인
- 공식 출처: Standard/Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-timeouts/
- 특이사항: timeouts.request:5s Accepted=True 이나 /delay/8이 8.0s 200. 카탈로그에 timeout iRule 없음

## 2.39

- 번호: 2.39
- 항목: HTTP Routing
- 중분류: HTTP Timeouts
- 세부항목: backendRequest
- 설명: Gateway에서 backend로 보내는 개별 요청 시간을 제한
- F5 지원: X
- 테스트 시나리오(명세파일 등): 정상 응답, backendRequest 초과 시 timeout, backendRequest가 request보다 크면 Accepted=False인지 확인
- 공식 출처: Standard/Extended | https://gateway-api.sigs.k8s.io/guides/user-guides/http-timeouts/
- 특이사항: backendRequest:2s Accepted=True 이나 /delay/4가 4.0s 200. backendRequest>request는 CRD CEL 거부. 카탈로그에 timeout iRule 없음

## 2.40

- 번호: 2.40
- 항목: HTTP Routing
- 중분류: HTTP Retry
- 세부항목: codes
- 설명: 재시도할 HTTP 상태코드 지정; 500/502/503/504는 필수 지원 대상
- F5 지원: -
- 테스트 시나리오(명세파일 등): 지정 상태코드만 재시도되고 그 외는 즉시 반환되는지, codes 중복 시 스키마 거부되는지 확인
- 공식 출처: Experimental/Extended | v1.6 validation | https://gateway-api.sigs.k8s.io/geps/gep-1731/
- 특이사항: 기능 미지원

## 2.41

- 번호: 2.41
- 항목: HTTP Routing
- 중분류: HTTP Retry
- 세부항목: attempts
- 설명: backend 요청의 최대 재시도 횟수 지정
- F5 지원: -
- 테스트 시나리오(명세파일 등): 최대 재시도 횟수와 attempts=0 스키마 거부 여부 확인
- 공식 출처: Experimental/Extended | v1.6 validation | https://gateway-api.sigs.k8s.io/geps/gep-1731/
- 특이사항: 기능 미지원

## 2.42

- 번호: 2.42
- 항목: HTTP Routing
- 중분류: HTTP Retry
- 세부항목: backoff
- 설명: 재시도 간 최소 대기 시간 지정
- F5 지원: -
- 테스트 시나리오(명세파일 등): 재시도 최소 대기 시간과 request timeout 내 완료 여부 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1731/
- 특이사항: 기능 미지원

## 2.43

- 번호: 2.43
- 항목: HTTP Routing
- 중분류: Session Persistence
- 세부항목: type: Cookie
- 설명: Gateway가 발급한 cookie로 동일 backend Pod에 세션 고정
- F5 지원: -
- 테스트 시나리오(명세파일 등): Set-Cookie 발급 후 반복 호출 시 동일 backend 고정 및 lifetime 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/
- 특이사항: 기능 미지원

## 2.44

- 번호: 2.44
- 항목: HTTP Routing
- 중분류: Session Persistence
- 세부항목: type: Header
- 설명: 지정 header 값을 이용하여 동일 backend Pod에 세션 고정
- F5 지원: -
- 테스트 시나리오(명세파일 등): 동일 header 값의 backend 고정과 서로 다른 값의 독립 세션 여부 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/
- 특이사항: 기능 미지원

## 2.45

- 번호: 2.45
- 항목: HTTP Routing
- 중분류: HTTP Route Rule
- 세부항목: rules[].name
- 설명: Route 내부 rule을 식별하는 고유 name 지정
- F5 지원: O
- 테스트 시나리오(명세파일 등): rule name별 전달과 동일 Route 내 name 중복 시 스키마 거부 여부 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/reference/api-types/httproute/

## 3.1

- 번호: 3.1
- 항목: Advanced Features
- 중분류: Cross-Namespace Routing
- 세부항목: Route parentRef
- 설명: 다른 namespace의 Gateway listener에 Route를 연결
- F5 지원: x
- 테스트 시나리오(명세파일 등): 다른 namespace Route가 Selector로 허용될 때 전달 및 Accepted=True 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/cross-namespace-routing/
- 특이사항: BNK 2.3: from=Selector는 Accepted되지만 미적용. unlabeled ns Route도 Accepted+전달(Selector가 All처럼 동작)

## 3.2

- 번호: 3.2
- 항목: Advanced Features
- 중분류: Cross-Namespace Routing
- 세부항목: Route backendRef
- 설명: 다른 namespace의 backend를 ReferenceGrant로 참조
- F5 지원: O
- 테스트 시나리오(명세파일 등): 다른 namespace backend를 ReferenceGrant로 참조할 때 전달 및 ResolvedRefs=True 확인
- 공식 출처: 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/referencegrant/

## 3.3

- 번호: 3.3
- 항목: Advanced Features
- 중분류: TLSRoute
- 세부항목: hostnames (SNI)
- 설명: TLS ClientHello의 SNI hostname으로 backend를 선택
- F5 지원: x
- 테스트 시나리오(명세파일 등): 일치 SNI는 지정 backend로 선택되고, 불일치 SNI는 매칭 실패하는지 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/
- 특이사항: TLS route 미지원

## 3.4

- 번호: 3.4
- 항목: Advanced Features
- 중분류: TLSRoute
- 세부항목: mode: Passthrough
- 설명: Gateway가 TLS를 종료하지 않고 암호화 stream을 backend로 전달
- F5 지원: O (F5 CRD)
- 테스트 시나리오(명세파일 등): Gateway가 TLS를 종료하지 않고 백엔드 인증서가 보이며 암호화 stream이 전달되는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/reference/api-types/tlsroute/
- 특이사항: HTTP route 의 tls.mode : passthrough 미지원

## 3.5

- 번호: 3.5
- 항목: Advanced Features
- 중분류: TLSRoute
- 세부항목: mode: Terminate
- 설명: Gateway에서 TLS를 종료한 후 backend로 전달
- F5 지원: O
- 테스트 시나리오(명세파일 등): Gateway 인증서로 TLS 종료 후 HTTP 전달, HTTP 80으로는 해당 listener가 쓰이지 않는지 확인
- 공식 출처: Extended | 기존 Terminate 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/tls/
- 특이사항: TLSRoute kind가 아니라 Gateway HTTPS listener + tls.mode Terminate + HTTPRoute + Secret. VIP cert=Secret, backend HTTP 200. 이전 BNK와 동일한 native terminate.

## 3.6

- 번호: 3.6
- 항목: Advanced Features
- 중분류: TLSRoute
- 세부항목: backendRefs.weight
- 설명: TLSRoute에서 복수 backend로 상대 weight 분산
- F5 지원: O(F5 CRD, tls terminate)
- 테스트 시나리오(명세파일 등): 동일 SNI 반복 연결의 weight 분산 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- 특이사항: TLS route 미지원, http route 와 crd 의 TCP route 로 weight 분산 가능

## 3.7

- 번호: 3.7
- 항목: Advanced Features
- 중분류: BackendTLSPolicy
- 세부항목: hostname / subjectAltNames
- 설명: upstream TLS SNI와 서버 인증서 hostname/SAN 검증
- F5 지원: x
- 테스트 시나리오(명세파일 등): hostname/SAN 일치 시 성공, 불일치 시 fail-close 및 policy status 오류 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html?highlight=backendtlspolicy 
  F5 CRD 로도 미지원

## 3.8

- 번호: 3.8
- 항목: Advanced Features
- 중분류: BackendTLSPolicy
- 세부항목: caCertificateRefs
- 설명: ConfigMap의 명시적 CA bundle로 upstream 서버 인증서 검증
- F5 지원: x
- 테스트 시나리오(명세파일 등): 지정 CA bundle로 upstream 인증서 검증 성공·실패 여부 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html?highlight=backendtlspolicy 
  F5 CRD 로도 미지원

## 3.9

- 번호: 3.9
- 항목: Advanced Features
- 중분류: BackendTLSPolicy
- 세부항목: wellKnownCACertificates: System
- 설명: 구현체의 system trust store를 이용해 upstream 인증서 검증
- F5 지원: x
- 테스트 시나리오(명세파일 등): 시스템 CA로 검증 시 사설 인증서는 실패, 공인 인증서 백엔드는 성공하는지 확인
- 공식 출처: Standard | https://gateway-api.sigs.k8s.io/reference/api-types/policy/backendtlspolicy/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html?highlight=backendtlspolicy 
  F5 CRD 로도 미지원

## 3.10

- 번호: 3.10
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: method.service / method.method
- 설명: gRPC service 및 method 이름으로 요청 분기
- F5 지원: X
- 테스트 시나리오(명세파일 등): 지정 gRPC method는 전달되고, 다른 method·일반 HTTP는 매칭되지 않는지 확인
- 공식 출처: Core | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/grpc-routing/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html 
  GPRC mutilple rule 미지원 
  Hostnames, Matches, Filters, SessionPersistence parameters in GRPCRoute CR are not supported.

## 3.11

- 번호: 3.11
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: headers (Exact/Regex)
- 설명: gRPC metadata header 값으로 요청 분기
- F5 지원: x
- 테스트 시나리오(명세파일 등): Exact/Regex header에 따른 backend 분기와 헤더 없음 시 default, regex 미지원 시 Route status 확인
- 공식 출처: Core/Implementation-specific | 기존 v1.4 판단 유지 | https://gateway-api.sigs.k8s.io/guides/user-guides/grpc-routing/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html 
  GPRC mutilple rule 미지원 
  Hostnames, Matches, Filters, SessionPersistence parameters in GRPCRoute CR are not supported.

## 3.12

- 번호: 3.12
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: Request/ResponseHeaderModifier
- 설명: gRPC 요청·응답 metadata header 추가/수정/삭제
- F5 지원: x
- 테스트 시나리오(명세파일 등): request header 추가와 response header 추가 결과 확인
- 공식 출처: Core/Extended | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html 
  GPRC mutilple rule 미지원 
  Hostnames, Matches, Filters, SessionPersistence parameters in GRPCRoute CR are not supported.

## 3.13

- 번호: 3.13
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: RequestMirror
- 설명: gRPC 요청을 mirror backend로 복제하고 mirror 응답은 무시
- F5 지원: x
- 테스트 시나리오(명세파일 등): 주 backend 응답 유지, mirror 수신 및 percent 비율 확인
- 공식 출처: Extended | https://gateway-api.sigs.k8s.io/geps/gep-3171/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html 
  GPRC mutilple rule 미지원 
  Hostnames, Matches, Filters, SessionPersistence parameters in GRPCRoute CR are not supported.

## 3.14

- 번호: 3.14
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: backendRefs.weight
- 설명: 복수 gRPC backendRef로 상대 weight 분산
- F5 지원: O
- 테스트 시나리오(명세파일 등): 반복 RPC 호출의 weight 분산 확인
- 공식 출처: Core | https://gateway-api.sigs.k8s.io/reference/api-spec/main/spec/

## 3.15

- 번호: 3.15
- 항목: Advanced Features
- 중분류: GRPCRoute
- 세부항목: sessionPersistence
- 설명: Cookie 또는 Header 기반으로 gRPC 세션을 동일 backend에 고정
- F5 지원: x
- 테스트 시나리오(명세파일 등): 쿠키 발급 후 동일 쿠키 재전송 시 동일 backend 고정 여부 확인
- 공식 출처: Experimental/Extended | https://gateway-api.sigs.k8s.io/geps/gep-1619/
- 특이사항: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html 
  GPRC mutilple rule 미지원 
  Hostnames, Matches, Filters, SessionPersistence parameters in GRPCRoute CR are not supported.

## 3.16

- 번호: 3.16
- 항목: Advanced Features
- 중분류: TCPRoute
- 세부항목: listener / parentRef
- 설명: TCP listener port에 TCPRoute를 연결하여 raw TCP stream 전달
- F5 지원: O (F5 CRD)
- 테스트 시나리오(명세파일 등): ncurity에서 listener port별 raw TCP 확인. Kind는 L4Route(TCPRoute 아님)
  `curl -sS http://40.30.20.20/` → `COFFEE SERVER - 30.0.0.10`
  `curl -sS http://40.30.20.20:8080/` → `TEA SERVER - 30.0.0.11`
  Gateway `supportedKinds=L4Route`, Programmed=True
- 공식 출처: v1.6 Standard/GA | 기존 v1.4 판단 유지 | https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.0
- 특이사항: TCPRoute kind 미지원. BNK native L4Route. :80 coffee / :8080 tea. weight 70/30 (40회 28/12)
  https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html 
  L4 route만 지원

## 3.17

- 번호: 3.17
- 항목: Advanced Features
- 중분류: TCPRoute
- 세부항목: backendRefs.weight
- 설명: 복수 TCP backendRef로 상대 weight 연결 분산
- F5 지원: O (F5 CRD)
- 테스트 시나리오(명세파일 등): ncurity에서 VIP :80 40회 curl 후 coffee/tea 비율 확인
  `for i in $(seq 1 40); do curl -sS http://40.30.20.20/; done | sort | uniq -c`
  기대: `COFFEE SERVER - 30.0.0.10` / `TEA SERVER - 30.0.0.11` 약 70/30. live 40회 coffee 28 / tea 12
- 공식 출처: v1.6 Standard/Core | https://gateway-api.sigs.k8s.io/guides/user-guides/tcp/
- 특이사항: TCPRoute kind 미지원. BNK native L4Route. :80 coffee / :8080 tea. weight 70/30 (40회 28/12)
  https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html 
  L4 route만 지원

## 3.18

- 번호: 3.18
- 항목: Advanced Features
- 중분류: UDPRoute
- 세부항목: listener / parentRef
- 설명: UDP listener port에 UDPRoute를 연결하여 datagram 전달
- F5 지원: O (F5 CRD)
- 테스트 시나리오(명세파일 등): ncurity에서 VIP :9053 UDP 확인. Kind는 L4Route(UDPRoute 아님)
  `echo -n ping | nc -u -w 2 40.30.20.20 9053; echo` → `COFFEE UDP - 30.0.0.10 ping`
  L4(`vs-bnk`)가 TCP-only면 ICMP unreachable/timeout. L4에 UDP VS가 있으면 위 명령으로 확인.
- 공식 출처: v1.6 Standard/GA | 기존 v1.4 판단 유지 | https://github.com/kubernetes-sigs/gateway-api/releases/tag/v1.6.0
- 특이사항: UDPRoute kind 미지원. BNK native L4Route UDP :9053 echo. weight ~70/30 (40회 27/13)
  https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html 
  L4 route만 지원

## 3.19

- 번호: 3.19
- 항목: Advanced Features
- 중분류: UDPRoute
- 세부항목: backendRefs.weight
- 설명: 복수 UDP backendRef로 상대 weight datagram 분산
- F5 지원: O (F5 CRD)
- 테스트 시나리오(명세파일 등): ncurity에서 VIP :9053 40회 UDP 후 coffee/tea 비율 확인
  `for i in $(seq 1 40); do echo -n ping | nc -u -w 2 40.30.20.20 9053; echo; done`
  기대: `COFFEE UDP - 30.0.0.10 ping` / `TEA UDP - 30.0.0.11 ping` 약 70/30. live 40회 coffee 27 / tea 13
- 공식 출처: v1.6 Standard/Core | https://gateway-api.sigs.k8s.io/guides/user-guides/udp/
- 특이사항: UDPRoute kind 미지원. BNK native L4Route UDP :9053 echo. weight ~70/30 (40회 27/13)
  https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html 
  L4 route만 지원
