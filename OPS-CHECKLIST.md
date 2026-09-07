# BNK 2.3 ALB 운영 체크리스트

Gateway API 2.x/3.x 라우팅 스펙 리뷰와 **겹치지 않는** day-2 운영 항목만 다룬다.  
path / hostname / header / method / weight / redirect / rewrite / CORS / timeout 필드 자체는 여기 없음 (`F5_Gateway_API_KO_apigw_v1.6.md` 참고).

랩: GatewayClass `f5-bnk-gateway-class`, VIP `40.30.20.20`, backend는 in-cluster Service가 아니라 F5 `Pool` (`k8s.f5net.com/v1`) static member `30.0.0.10/11/12`.  
VIP 앞단에 L4 ECMP 있음.  
근거: 클러스터 `kubectl explain` / `kubectl get crd`, [외부 Pool](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/how-tos/configure-external-resource-load-balancing.html), [HTTPRoute](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-httproute.html), [GRPCRoute](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html), [L4Route](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html), [Gateway](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html), [Debug sidecar](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/troubleshooting/spk-tmm-debug.html).

상태 표시:

| 표시 | 의미 |
|---|---|
| **클러스터 CRD로 가능** | 이 클러스터 CRD/`kubectl explain`에 필드·Kind가 있음 |
| **문서상 가능 미검증** | clouddocs 또는 CRD는 있으나 이 랩에서 apply/트래픽으로 확인하지 않음 |
| **이 랩에서 확인 불가** | 도구·테이블·환경이 없거나, 동작 여부를 아직 모름 |
| **Gateway API 미지원** | HTTPRoute/GRPCRoute 필드 없거나 BNK가 무시/거부 |
| **classic BIG-IP만** | TMOS VS/Pool 노브. BNK Pool/Gateway CRD에 없음 |

---

## 1. 목적 / 범위

- ALB로 쓰는 BNK의 **모니터, 멤버 빼기, service down, SNAT, persist, 로그, iRule, AFM, 인증서, TMM 스케일, VIP 장애** 점검.
- 하지 않는 것: Helm/이미지 변경, 트래픽 테스트 apply, Gateway API 라우팅 항목 재검증.

---

## 2. 설정 확인 방법 (configview로는 정상 모니터링 불가)

시트 2.2 K: VS에는 default pool만 보이고, configview pool에 다른 멤버가 있어도 **VS 매핑·경로가 안 나온다**. 경로별 pool 분기를 configview로 확인하지 말 것.

### 볼 수 있는 것

- [ ] `kubectl get gateway,httproute,grpcroute,l4route -n web`  
  Gateway `Programmed=True`, Route `Accepted` / `ResolvedRefs`.
- [ ] `kubectl get pool -n web` 및 `-o yaml`  
  `status.conditions` `READY=True`, message `CR config sent to all grpc endpoints`.  
  **READY는 TMM에 CR이 전달됐다는 뜻이지, 멤버 up/down이 아니다.** Pool status에 member health 필드 없음.
- [ ] `kubectl describe pool <name> -n web` — spec(members, monitors, minActiveMembers)과 condition만.
- [ ] Controller: `kubectl logs -n f5-bnk-instance deploy/f5-cne-controller`  
  pool create 시 `service_down_action` 등 내부 필드가 로그에 남을 수 있음 (설정 UI 아님).
- [ ] TMM 로그: `kubectl logs -n f5-bnk-instance <f5-tmm-*> -c f5-tmm`
- [ ] TMM debug (`kubectl exec -n f5-bnk-instance <f5-tmm-*> -c debug -- …`):
  - `tmctl -d blade virtual_server_stat -s name,clientside.tot_conns`
  - `tmctl -d blade pool_stat` (`pick_tot`, `pick_rej`)
  - `tmctl -d blade pool_member_stat -s pool_name,serverside.tot_conns`
  - `bdt_cli -u -s tmm0:8850 connection list`
  - `bdt_cli -u -s tmm0:8850 route` / `arp`
- [ ] 실제 전달은 클라이언트로 확인 (Host/Path별 body). 설정 뷰가 아님.

### 볼 수 없는 것 / 쓰지 말 것

- [ ] **configview**: path → pool, rule → member 매핑. 시트 2.2와 동일. VS default pool + 고아 pool member만 보이면 정상처럼 보여도 **운영 확인으로 쓰지 말 것**.
- [ ] tmctl `monitor_stat` / `monitor_instance_stat` / `pool_member_monitor_stat`: 이 TMM에 **테이블 없음**. 멤버별 probe 성공/실패를 tmctl로 못 봄.
- [ ] tmctl `pool_member_stat`의 `status` / `session_status` 컬럼: **없음**. 전 컬럼은 커넥션/PVA/hornet 카운터 + `flags`(이 랩 web 멤버는 전부 0).
- [ ] Pool CR status의 per-member up/down: **없음**.
- [ ] classic `tmsh list ltm virtual` / iControl REST: 없음.

**모니터 결과 가시성: 없음.** `spec.monitors.http`는 TMM에 내려가지만 (configview `ltm_monitor`에 interval/send/recv만 있음) **현재 멤버 up/down, last probe, session disable를 조회하는 API/테이블/대시보드는 없다.**  
예외는 TMM 이벤트 로그뿐: `kubectl logs -n f5-bnk-instance <f5-tmm-*> -c f5-tmm | grep '01010057'` → `Pool Member Status Change: … is up|down`. 전이 기록이지 현재 상태 조회가 아니고, Pool CR status에도 반영되지 않음. `pool_stat.pick_rej_monitor`는 모니터 때문에 pick이 거절된 **누적 카운터**이지 멤버 상태가 아님.

공식 debug: [spk-tmm-debug](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/troubleshooting/spk-tmm-debug.html).

---

## 3. Health monitor

**클러스터 CRD로 가능.** `Pool.spec.monitors` (별도 Monitor CRD 없음). 공식: 외부 엔드포인트는 K8s probe가 없으므로 Pool monitor를 씀. 한 Route rule이 여러 Pool을 참조하면 **monitor 설정이 서로 같아야** 함.

| 타입 | 주요 필드 | 용도 |
|---|---|---|
| `http` | interval, timeout, sendString, receiveString, receiveDisableString, username, password | HTTP ALB (2.1 YAML에 이미 있음) |
| `http2` | 위 + serversslProfileName, timeUntilUp, upInterval | gRPC/h2 백엔드 |
| `tcp` | interval, timeout, send/receive, receiveDisableString | TCP/L4 |
| `tcpHalfOpen` | interval, timeout | SYN만 |
| `icmp` | interval, timeout | L3 |
| `dns` | queryName 필수, queryType, recvAddress 등 | DNS |
| `inband` | failures, failureInterval, responseTime, retryTime | 실트래픽 수동 모니터 |

체크:

- [ ] HTTP ALB: `spec.monitors.http` — `sendString` / `receiveString`이 백엔드 실제 응답과 맞는지. 2.1은 `GET /` + receive `200`.
- [ ] gRPC: `http`가 아니라 `http2`(+ TLS면 `serversslProfileName`)인지. **문서상 가능 미검증.**
- [ ] L4 TCP/UDP: `tcp` 또는 `tcpHalfOpen` / `icmp`. UDP에 HTTP 모니터를 붙이지 말 것.
- [ ] `receiveDisableString`: 응답 정규식 매칭 시 타깃 **disable** (CRD 설명). classic “disable string”에 해당. **문서상 가능 미검증.**
- [ ] inband: 액티브 모니터 없이 실패 횟수로 down. **문서상 가능 미검증.**
- [ ] 확인: Pool READY ≠ member up. **모니터 결과 가시성: 없음** (위 §2). kubectl/tmctl/configview/컨트롤러 메트릭에 멤버 health 필드 없음. 공식 노출은 TMM 로그 키 `PoolMemberStatus` (UP/DOWN 이벤트)뿐. 운영에서 “지금 up인가”를 보려면 명령을 놓친 게 아니라 **제품 갭**.

---

## 4. Pool member disable / enable

`Pool.spec.members` = `address` + `port` + 선택 `priorityGroup`만.  
**session disable / force offline / monitor disable 필드 없음.** **classic BIG-IP만** (또는 아래 우회).

| 하고 싶은 일 | 이 클러스터에서 |
|---|---|
| 멤버 빼기 | YAML에서 해당 `members[]` 삭제 후 apply. 신규 연결 중단. 기존 세션 유지(session disable)는 **CRD에 없음** |
| 다시 넣기 | `members[]` 복구 |
| 모니터로 disable | `receiveDisableString`이 매칭되면 disable. **문서상 가능 미검증.** 운영자가 버튼으로 끄는 것과 다름 |
| 강제 down 시뮬레이션 | 백엔드 프로세스 중지 → 모니터 fail. disable이 아니라 **monitor down** |

체크:

- [ ] 점검 빼기는 `members`에서 제거. “Disabled” 상태가 Pool status에 안 남음.
- [ ] 확인은 `kubectl get pool -o yaml`의 members 목록 + 트래픽이 남은 멤버로만 가는지. configview/tmctl session_status는 사용 불가.
- [ ] 여러 멤버인 Pool에서 하나 빼기/넣기는 이 랩 기본 YAML이 멤버 1개라 **바로 검증하려면 Pool을 잠시 멀티멤버로 바꿔야 함** (트래픽 apply는 이 문서 범위 밖).

---

## 5. Action on service down

`Pool.spec`에 `serviceDownAction` / `service_down_action` **필드 없음.**

- 레거시 SPK `F5SPKIngressTCP/UDP`에는 `serviceDownAction` (`NONE` / `REJECT` / `DROP` / `RESELECT`)이 문서화되어 있으나, **이 클러스터에 해당 Ingress CRD 없음.**
- 컨트롤러가 pool 생성 시 로그에 `service_down_action: POOLMBR_ACTION_RESELECT`를 남긴 것은 **하드코딩 기본값으로 보임.** CR로 바꿀 수 없음.

체크:

- [ ] 기대 동작(RESELECT = 다른 멤버로 재선택)을 바꾸려면 **클러스터 CRD로 불가.**
- [ ] 멤버 1개인 이 랩 Pool에서는 RESELECT할 대상이 없어, down 시 500/연결 실패와 구분하기 어려움. **이 랩에서 확인 불가** (멀티멤버 + 모니터 down 필요).
- [ ] classic `action on service down` (None/Reject/Drop/Reselect) UI = **classic BIG-IP만.**

---

## 6. 그 외 운영 체크리스트

### 6.1 SNAT

1. **Ingress SNAT Automap / None** — **문서상 가능 미검증.**  
   Gateway `spec.infrastructure.annotations."k8s.f5.com/snat-type"` = `Automap`(기본, 소스=TMM IP) 또는 `None`(클라이언트 IP 유지).  
   [Gateway CR](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html).  
   이 TMM `tmctl pool_stat`에 `snat_automap[0]`가 이미 있음 (시스템 객체).
2. **Ingress SNAT pool (고정 SNAT IP 목록)** — **classic BIG-IP만** / Ingress CRD에 없음.  
   `F5SPKSnatpool`은 문서상 **egress** 전용 (`F5SPKEgress`와 쌍). ALB VIP→백엔드 SNAT pool이 아님.
3. **Egress SNAT** — **클러스터 CRD로 가능**, ALB 인바운드와 별개. 이 랩에 Snatpool/Egress CR 없음.

백엔드가 클라이언트 원본 IP를 봐야 하면 `None`을 검토. 랩 백엔드 `30.0.0.10/11/12`에서 소스 IP를 아직 대조하지 않음.

### 6.2 Persistence (쿠키 / 소스 IP)

4. **HTTPRoute/GRPCRoute `sessionPersistence`** — **Gateway API 미지원.**  
   클러스터 HTTPRoute/GRPCRoute CRD에 필드 없음 (v1.6.1). 시트 2.43/2.44 experimental 제외, 3.15 unknown field. 카탈로그 persist iRule 없음 (`backend/IRULE-MAP.md`).
5. **BackendLBPolicy** (`sessionPersistence` Cookie/Header) — CRD는 있음. BNK Gateway/HTTPRoute 문서에 attach 방법 없음. **이 랩에서 확인 불가** (적용해도 컨트롤러가 무시할 가능성 큼).
6. **F5 persist profile CRD** — 클러스터에 없음. **classic BIG-IP만.**
7. **소스 IP persist** — Pool/Gateway CRD에 없음. **classic BIG-IP만.**

F5 쪽 대안: persist 전용 CRD/iRule **없음**. 고정이 필요하면 앱 쿠키 또는 단일 멤버 Pool뿐.

### 6.3 Connection limit / slow ramp / LB 알고리즘

8. **connection limit (VS/member)** — Pool/Gateway에 없음. **classic BIG-IP만.**
9. **slow ramp time** — 없음. **classic BIG-IP만.**
10. **loadBalancingMethod** (least conn 등) — Pool CRD에 없음. 레거시 SPK Ingress에만 문서화. 기본은 RR + Route `weight`. **classic BIG-IP만** (weight는 라우팅 시트).

### 6.4 Priority group / minActiveMembers

11. **`members[].priorityGroup`** — **클러스터 CRD로 가능.** 높은 그룹 우선.
12. **`minActiveMembers`** — **클러스터 CRD로 가능.** 그룹 활성화 최소 멤버 수.  
    둘 다 **문서상 가능 미검증.** 이 랩 Pool은 멤버 1개·priority 없음.

### 6.5 Logging / HSL

13. **F5BigLogHslpub + F5BigLogProfile + BNKSecPolicy** — **클러스터 CRD로 가능**, **문서상 가능 미검증.**  
    BNKSecPolicy `extensionRefs.kind` enum: `F5BigFwPolicy`, `F5BigLogProfile`, `F5BigDdosGlobal`.  
    LogProfile 필드는 firewall / NAT / DNS / ALG / protocolInspection 중심. **classic HTTP request log 프로필과 다름.**
14. **iRule `HSL::send`** — 카탈로그 HTTP 미러 우회용. gRPC 미검증 (`IRULE-MAP.md`).
15. **kubectl/TMM 로그** — 항상 가능. HSL 대체 아님.

### 6.6 iRule attach

16. **F5BigCneIrule + BNKNetPolicy** — **클러스터 CRD로 가능.**  
    `extensionRefs`는 `F5BigCneIrule`만. `targetRefs`는 Gateway (+ `sectionName`이면 listener). 경로/`backendRef` 단위 attach **없음**.  
    카탈로그: CORS/redirect/header/rewrite/HSL mirror (HTTP). persist/timeout/retry iRule **없음**.

### 6.7 WAF / AFM / DDoS

17. **AFM ACL** — `F5BigFwPolicy` (+ Rulelist) → `BNKSecPolicy` → Gateway/GatewayClass/listener. **클러스터 CRD로 가능**, **문서상 가능 미검증.**  
    [Firewall in Gateway API](https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/bnk-fwpolicy-in-gateway-api.html).
18. **DDoS** — `F5BigDdosGlobal` + BNKSecPolicy. **문서상 가능 미검증.**
19. **WAF / AWAF / ASM** — 클러스터에 WAF CRD 없음. Access(APM) CRD는 있으나 BNKNetPolicy/BNKSecPolicy enum에 없음. **classic BIG-IP만** (또는 별도 제품).

### 6.8 인증서 / Secret 로테이션

20. **클라이언트 TLS** — Gateway HTTPS `listeners.tls.certificateRefs` → `Secret` `kubernetes.io/tls`. **클러스터 CRD로 가능** (3.5 Terminate는 시트에서 동작). 로테이션: Secret 갱신 후 listener 상태 확인. hostname별 SNI 선택 실패는 라우팅 시트(3.3).
21. **백엔드 TLS (재암호화)** — BackendTLSPolicy는 CRD만 있고 컨트롤러 미처리 (3.7–3.9). **Gateway API 미지원.** Pool `http2.serversslProfileName`은 모니터용. **문서상 가능 미검증.**
22. **이 랩 인증서 파일** — `backend/certs/`. 비밀번호를 파일에 넣지 말 것.

### 6.9 TMM 스케일 / VIP 장애

23. **TMM 대수** — `daemonset/f5-tmm` Desired=2 (`f5-tmm-m6nhk`, `f5-tmm-ms995`). 스케일/이미지는 Helm — **이 레포에서 변경하지 않음.**
24. **VIP fail** — Gateway `status.addresses` + 양쪽 TMM debug에서 VS/pool 카운터. 앞단 L4 ECMP가 TMM `172.24.0.10/.11`으로 분산. ECMP 자체는 이 체크리스트 범위 밖.
25. **VIP 변경** — 문서: `infrastructure.parametersRef` 바꾸면 Gateway 삭제 후 재생성. 이 랩은 static `40.30.20.20`.

### 6.10 UDP / TCP vs HTTP 운영 차이

26. **TCP/UDP 라우트** — 커뮤니티 TCPRoute/UDPRoute는 BNK가 거부. **L4Route** (`gateway.k8s.f5net.com/v1`). listener `kinds.group` 필수. **클러스터 CRD로 가능.**
27. **L4 모니터** — `tcp` / `tcpHalfOpen` / `icmp`. HTTP `sendString` 쓰지 말 것.
28. **L4에 없는 것** — path/header/hostname, HTTP iRule 이벤트, 쿠키 persist.
29. **권장** — HTTP / gRPC / L4는 listener 분리. L4·GRPC는 listener당 Route 1개·backendRef 1개 (공식).
30. **`pvaAccelerationMode`** — L4Route만. **문서상 가능 미검증.**

### 6.11 이미 시트에서 깨진 운영 노브 (라우팅 재테스트 아님)

31. **HTTP timeout / retry** — 필드 Accepted여도 미적용 (2.38–2.39). iRule 없음. **Gateway API 미지원**에 가깝다.
32. **BackendTLSPolicy** — 재암호화 운영 불가 (3.7–3.9).

### 6.12 기타 CRD (ALB와 거리 있음)

33. **`dynamicMembers`** — Service Endpoint를 Pool에 합침. 이 랩은 static만. **클러스터 CRD로 가능.**
34. **F5BigAnalyzer** — GPU/LLM weight. ALB 일반 운영 아님.
35. **OneConnect / HTTP profile / VS 커넥션 큐** — CRD 없음. **classic BIG-IP만.**

---

## 7. 이 랩에서 바로 볼 수 있는 것 vs 운영에서만 의미 있는 것

### 이 랩에서 바로 (기존 2.1 Pool + kubectl/tmctl, 새 트래픽 apply 없이)

- [ ] `kubectl explain pool.spec` / `pool.spec.monitors` / `pool.spec.members` — 필드 존재 확인.
- [ ] `kubectl get crd` — Pool, BNKNetPolicy, BNKSecPolicy, F5BigCneIrule, F5BigFwPolicy, F5BigLog*, F5SPKSnatpool, L4Route.
- [ ] 2.1이 apply된 상태라면: Pool READY, `spec.monitors.http` 3개, Gateway Programmed.
- [ ] TMM debug: `virtual_server_stat`, `pool_stat`, `pool_member_stat` (커넥션 카운터만). 모니터 테이블 없음 재확인.
- [ ] configview를 경로 확인에 쓰지 말 것 (2.2).
- [ ] 멤버 1개 Pool에서는 disable/RESELECT/priority group을 체감하기 어려움.

### 운영(또는 별도 검증 창)에서만 의미 있는 것

- 멀티멤버 + 모니터 down → RESELECT / 500 구분.
- `k8s.f5.com/snat-type: None` 후 백엔드 access log의 소스 IP.
- `priorityGroup` + `minActiveMembers` failover.
- `receiveDisableString` / inband / http2 모니터.
- BNKSecPolicy + FwPolicy + HSL (원격 로그 서버 필요).
- iRule을 운영 예외 처리에 쓸지 (listener 전역).
- Secret 로테이션, TMM 노드 장애, 앞단 ECMP 한쪽 down.
- 쿠키 persist — CRD/iRule 공백. 앱 계층으로 갈지 결정.

---

## 공식 링크 (라우팅 시트와 별도)

- Pool / 외부 LB: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/how-tos/configure-external-resource-load-balancing.html
- HTTPRoute: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-httproute.html
- GRPCRoute: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-grpcroute.html
- L4Route: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-l4route.html
- Gateway (SNAT annotation): https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-gateway-api-gateway.html
- CRD 목록: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/spk-custom-resources.html
- BNKNetPolicy / iRule: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-bnkNetPolicy.html
- BNKSecPolicy: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/bnk-bnkSecPolicy.html
- F5SPKSnatpool (egress): https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/custom-resource-definitions/spk-snatpool-crd.html
- Debug / tmctl / configview: https://clouddocs.f5.com/bigip-next-for-kubernetes/latest/troubleshooting/spk-tmm-debug.html
