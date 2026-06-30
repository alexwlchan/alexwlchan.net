#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

run_command 'ruff format assets mosaic scripts tests'

if [[ "${CI:-}" == "true" ]]
then
  run_command 'git diff --exit-code'
fi

run_command 'ruff check --fix assets mosaic scripts tests'
run_command 'ty check assets scripts'
run_command 'mypy mosaic tests'
run_command 'python3 scripts/build_site.py'
run_command "python3 -m pytest --cov -q tests"
