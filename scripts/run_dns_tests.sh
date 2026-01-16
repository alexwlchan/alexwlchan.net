#!/usr/bin/env bash

set -o errexit
set -o nounset

print_info() {
    echo -e "\033[34m$1\033[0m"
}

print_info "-> ruff format dns"
ruff format dns

echo ""

print_info "-> ruff check --fix dns"
ruff check --fix dns

echo ""

print_info "-> mypy dns"
mypy dns

echo ""

print_info "-> coverage run -m pytest dns"
coverage run -m pytest dns

echo ""

print_info "-> coverage report --include 'dns/*'"
coverage report --include 'dns/**'
