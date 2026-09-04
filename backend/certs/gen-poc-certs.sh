#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
  -keyout ca.key -out ca.crt -subj "/CN=poc-backend-ca"

openssl req -newkey rsa:2048 -nodes -keyout coffee.key -out coffee.csr \
  -subj "/CN=coffee.f5bnk.com"
printf 'subjectAltName=DNS:coffee.f5bnk.com\n' > coffee.ext
openssl x509 -req -in coffee.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out coffee.crt -days 3650 -extfile coffee.ext

openssl req -newkey rsa:2048 -nodes -keyout tea.key -out tea.csr \
  -subj "/CN=tea.f5bnk.com"
printf 'subjectAltName=DNS:tea.f5bnk.com\n' > tea.ext
openssl x509 -req -in tea.csr -CA ca.crt -CAkey ca.key -CAcreateserial \
  -out tea.crt -days 3650 -extfile tea.ext

cp coffee.crt gw-terminate.crt
cp coffee.key gw-terminate.key
rm -f coffee.csr tea.csr coffee.ext tea.ext ca.srl
echo "wrote certs in $PWD"
