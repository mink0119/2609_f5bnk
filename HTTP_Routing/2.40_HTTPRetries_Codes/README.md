# 2.40 HTTP Retry — codes

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|500/502/503/504 만 retry| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

### 1. 정상

```bash
curl -sS -D - -o /tmp/gw-body  --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/; echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- HTTP/1.1 200
- Body: `COFFEE SERVER - 30.0.0.10`

### 2. 선택 코드만 재시도

```bash
echo '백엔드가 503이면 재시도, 404면 재시도 없음. 중복 codes는 API 거부'
```

**기대 응답**
- 500/502/503/504 재시도
- 그 외 코드는 즉시 반환
- codes 중복 시 스키마 거부

## 정리

```bash
kubectl delete -f gw-http-route.yaml
```

## iRule 우회

네이티브 `retry.codes` 미적용. `gw-http-route_iRule.yaml` 은 `HTTP_REQUEST` 에서 `HTTP::request` 저장 후, `HTTP_RESPONSE` 에서 500/502/503/504 만 `HTTP::retry $req` 1회. 인자 없으면 TMM `Invalid number of arguments`. `/fail404` 는 재시도 없음.  
클라이언트 상태코드는 retry 증거가 아니다. `/fail`·`/fail500` 은 백엔드가 계속 같은 코드를 내므로 retry 해도 클라이언트는 503/500. 증명은 coffee `access_log` 히트 수.  
네이티브 YAML 과 같이 apply 하지 않는다.

```bash
kubectl apply -f gw-http-route_iRule.yaml
```

백엔드에서 로그를 연 뒤 클라이언트로 친다.

```bash
tail -f /var/log/nginx/poc-access.log
```

```bash
curl -sS -D - -o /tmp/gw-body --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
echo; echo '--- body ---'; cat /tmp/gw-body; echo
curl -sS -D - -o /tmp/gw-body --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/fail
echo; echo '--- body ---'; cat /tmp/gw-body; echo
curl -sS -D - -o /tmp/gw-body --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/fail500
echo; echo '--- body ---'; cat /tmp/gw-body; echo
curl -sS -D - -o /tmp/gw-body --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/fail404
echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- `GET /` → 200, access log 1회
- `/fail` → 클라이언트 503, access log **2회** (원요청 + retry 1)
- `/fail500` → 클라이언트 500, access log **2회**
- `/fail404` → 클라이언트 404, access log **1회** (codes 밖, retry 없음)

iRule 없이 같은 curl 이면 `/fail`·`/fail500` 도 1회. 그때와 히트 수가 달라야 2.40 우회가 맞다.

```bash
kubectl delete -f gw-http-route_iRule.yaml
```
