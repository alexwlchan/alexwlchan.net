#!/usr/bin/env bash

set -o errexit
set -o nounset

touch src/_tweets/auth.yml
echo "consumer_key: $(keyring get twitter consumer_api_key)"            > src/_tweets/auth.yml
echo "consumer_secret: $(keyring get twitter consumer_api_secret_key)" >> src/_tweets/auth.yml
echo "access_token: $(keyring get twitter access_token)"               >> src/_tweets/auth.yml
echo "token_secret: $(keyring get twitter access_token_secret)"        >> src/_tweets/auth.yml