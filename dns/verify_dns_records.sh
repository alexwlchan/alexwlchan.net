#!/usr/bin/env bash

set -o errexit
set -o nounset

export BUNDLE_WITH=check_dns

bundle install

cd "$(git rev-parse --show-toplevel)/dns"

saved_dns_records="dns_records.yml"
live_dns_records=$(bundle exec save_dns_records_as_yaml.rb)

bundle exec compare_dns_records.rb "$saved_dns_records" "$live_dns_records"
