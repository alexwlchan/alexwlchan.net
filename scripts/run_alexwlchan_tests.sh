#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

report_coverage() {
    echo ""
    echo -e "\033[34m-> python3 -m coverage report\033[0m"
    if [[ $(python3 -m coverage report --format=total) = "100" ]]
    then
        echo "100% coverage!"
    else
        python3 -m coverage report
    fi
}

run_command 'ruff format mosaic scripts tests'

if [[ "${CI:-}" == "true" ]]
then
  run_command 'git diff --exit-code'
fi

run_command 'ruff check --fix mosaic scripts tests'
run_command 'mypy mosaic scripts tests'
run_command 'python3 scripts/build_site.py'
run_command "python3 -m coverage run -m pytest -q tests"
report_coverage
