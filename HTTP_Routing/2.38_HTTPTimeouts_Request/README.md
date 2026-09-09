# 2.38 HTTP Timeouts — request

## 구성

```mermaid
flowchart LR
  C[Client] --> VIP[VIP]
  VIP -->|request 5s| P1[coffee-pool]
```

## 적용

```bash
kubectl apply -f gw-http-route-f1.yaml
```

명령은 VIP `40.30.20.20` 에 터널로 도달하는 클라이언트에서 실행합니다.

## 클라이언트 검증

```bash
curl -sS -D - -o /tmp/gw-body -w 'time=%{time_total}\n' --max-time 15 --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/
echo; echo '--- body ---'; cat /tmp/gw-body; echo
curl -sS -D - -o /tmp/gw-body -w 'time=%{time_total}\n' --max-time 15 --resolve coffee.f5bnk.com:80:40.30.20.20 http://coffee.f5bnk.com/delay/8
echo; echo '--- body ---'; cat /tmp/gw-body; echo
```

**기대 응답**
- `GET /` → 200 `COFFEE SERVER - 30.0.0.10`
- `/delay/8` → 8s 200 (`request: 5s` 미적용)

## 정리

```bash
kubectl delete -f gw-http-route-f1.yaml
```

## iRule 우회

네이티브 `timeouts.request: 5s` 미적용.  
`after 5000` 은 동작하지만 콜백의 `HTTP::respond` 는 무시된다. `TCP::respond` 504 + `TCP::close`. 정상 응답은 `HTTP_RESPONSE` 에서 `after cancel`.  
네이티브 YAML 과 같이 apply 하지 않는다.

```bash
kubectl apply -f gw-http-route_iRule.yaml
```

검증 명령은 위와 동일.

**기대 응답**
- `GET /` → 200 `COFFEE SERVER - 30.0.0.10`
- `/delay/8` → 504 `gateway timeout` (~5s)

```bash
kubectl delete -f gw-http-route_iRule.yaml
```
