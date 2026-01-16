#!/usr/bin/env bash

set -o errexit
set -o nounset

print_info() {
    echo -e "\033[34m$1\033[0m"
}

print_info "-> ruff format mosaic scripts tests"
ruff format mosaic scripts tests

echo ""

print_info "-> ruff check --fix mosaic scripts tests"
ruff check --fix mosaic scripts tests

echo ""

print_info "-> mypy mosaic scripts tests"
mypy mosaic scripts tests

echo ""

print_info "-> coverage run -m pytest tests"
coverage run -m pytest tests

echo ""

print_info "-> coverage report --include 'mosaic/*,tests/*'"
coverage report --include 'mosaic/*,tests/*'
