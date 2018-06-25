#!/usr/bin/env bash

set -o errexit
set -o nounset

DOMAIN="$1"

chmod 600 cloudflare_credentials

docker run \
  # https://certbot.eff.org/docs/using.html#id6 ("Lock Files")
  --volume ~/letsencrypt/config:/etc/letsencrypt \
  --volume ~/letsencrypt/work:/var/lib/letsencrypt \
  --volume ~/letsencrypt/logs:/var/log/letsencrypt \

  # Provides CloudFlare credentials
  -v $(pwd):/certs alexwlchan/certbot \

  certonly --domain "*.$DOMAIN" \

    # Required if you're requesting wildcard certs
    --server https://acme-v02.api.letsencrypt.org/directory \

    --dns-cloudflare --dns-cloudflare-credentials=/certs/cloudflare_credentials \
    --non-interactive --agree-tos --email=certbot@alexwlchan.fastmail.co.uk
