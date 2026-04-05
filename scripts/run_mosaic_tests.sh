#!/usr/bin/env bash

set -o errexit
set -o nounset

print_info() {
    echo -e "\033[34m$1\033[0m"
}

print_info "-> ruff format mosaic scripts tests uptime_tests"
ruff format mosaic scripts tests uptime_tests

echo ""

if [[ "${CI:-}" == "true" ]]
then
  print_info "-> git diff --exit-code"
  git diff --exit-code

  echo ""
fi

print_info "-> ruff check --fix mosaic scripts tests uptime_tests"
ruff check --fix mosaic scripts tests uptime_tests

echo ""

print_info "-> mypy mosaic scripts tests"
mypy mosaic scripts tests

echo ""

# These have to be separate so Mypy doesn't get confused by the two
# files named `conftest.py`
print_info "-> mypy uptime_tests"
mypy uptime_tests

echo ""

print_info "-> python3 -m pytest --cov=mosaic -n=auto"
python3 -m pytest tests --cov=mosaic -n=auto

echo ""

print_info "-> coverage report --include 'mosaic/*,tests/*'"
coverage report --include 'mosaic/*,tests/*'
