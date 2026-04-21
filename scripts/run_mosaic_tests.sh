#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

run_command 'ruff format mosaic scripts tests uptime_tests'

if [[ "${CI:-}" == "true" ]]
then
  run_command 'git diff --exit-code'
fi

run_command 'ruff check --fix mosaic scripts tests uptime_tests'
run_command 'mypy mosaic scripts tests'

# These have to be separate so Mypy doesn't get confused by the two
# files named `conftest.py`
run_command "mypy uptime_tests"

run_command "python3 -m coverage run -m pytest -q tests"
run_command "python3 -m coverage report"
