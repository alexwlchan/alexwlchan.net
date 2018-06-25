#!/usr/bin/env bash

set -o errexit
set -o nounset

DOMAIN="$1"

chmod 600 "$CERTS"/cloudflare_credentials

docker run \
  --volume ~/letsencrypt/config:/etc/letsencrypt \
  --volume ~/letsencrypt/work:/var/lib/letsencrypt \
  --volume ~/letsencrypt/logs:/var/log/letsencrypt \
  --volume "$CERTS":/certs alexwlchan/certbot \
  certonly --domain '*.'$DOMAIN \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --dns-cloudflare --dns-cloudflare-credentials=/certs/cloudflare_credentials \
    --non-interactive --agree-tos --email=certbot@alexwlchan.fastmail.co.uk
