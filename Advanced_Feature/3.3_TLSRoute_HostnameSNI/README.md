# 3.3 TLSRoute — hostname SNI

TLSRoute / protocol TLS 는 BNK에서 미지원.  
BNK native 시도: HTTPS listener `hostname:` + Secret 두 개 (coffee / tea) 와 HTTPRoute hostnames.

## 구성

```mermaid
flowchart LR
  C["SNI/Host coffee / tea"] --> GW["tls-gw HTTPS Terminate"]
  GW -->|coffee.f5bnk.com| P1[coffee-pool :80]
  GW -->|tea.f5bnk.com| P2[tea-pool :80]
```

## 적용

```bash
kubectl apply -f gw-tls-route.yaml
```

## 클라이언트 검증

```bash
echo | openssl s_client -connect 40.30.20.20:443 -servername coffee.f5bnk.com 2>/dev/null | openssl x509 -noout -subject
echo | openssl s_client -connect 40.30.20.20:443 -servername tea.f5bnk.com 2>/dev/null | openssl x509 -noout -subject
curl -k --resolve coffee.f5bnk.com:443:40.30.20.20 https://coffee.f5bnk.com/
curl -k --resolve tea.f5bnk.com:443:40.30.20.20 https://tea.f5bnk.com/
```

**live 결과 (재검증)**
- HTTP Host 라우팅: coffee → `COFFEE SERVER - 30.0.0.10`, tea → `TEA SERVER - 30.0.0.11`
- SNI 인증서 선택: 두 SNI 모두 `CN=tea.f5bnk.com` (listener hostname SNI 미적용, last-wins)

## 정리

```bash
kubectl delete -f gw-tls-route.yaml
```

## iRule 우회

HTTPS Terminate 의 last-wins 인증서는 iRule 로 안 고친다. iRule 은 TLS handshake 를 대신 하지 못하고, Secret/SSL profile 인증서를 바꿔 응답할 수도 없다.

`gw-tls-route_iRule.yaml` 은 3.4 와 같이 **TCP :443 + L4Route 패스스루**. `CLIENT_DATA` 에서 ClientHello 바이너리의 SNI(extension type 0)를 읽어 `pool web-pool-coffee-pool-pool` / `web-pool-tea-pool-pool`. 인증서는 백엔드 `coffee.crt` / `tea.crt`.  
네이티브 YAML 과 같이 apply 하지 않는다.

```bash
kubectl apply -f gw-tls-route_iRule.yaml
```

```bash
echo | openssl s_client -connect 40.30.20.20:443 -servername coffee.f5bnk.com 2>/dev/null | openssl x509 -noout -subject
echo | openssl s_client -connect 40.30.20.20:443 -servername tea.f5bnk.com 2>/dev/null | openssl x509 -noout -subject
curl -k --resolve coffee.f5bnk.com:443:40.30.20.20 https://coffee.f5bnk.com/
curl -k --resolve tea.f5bnk.com:443:40.30.20.20 https://tea.f5bnk.com/
```

**기대 응답**
- SNI `coffee.f5bnk.com` → `CN=coffee.f5bnk.com`, body `COFFEE TLS - 30.0.0.10`
- SNI `tea.f5bnk.com` → `CN=tea.f5bnk.com`, body `TEA TLS - 30.0.0.11`
- 불일치 SNI 는 매칭 실패 (`reject`)

```bash
kubectl delete -f gw-tls-route_iRule.yaml
```
