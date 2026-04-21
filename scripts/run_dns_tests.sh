#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

run_command "ruff format dns"
run_command "ruff check --fix dns"
run_command "mypy dns"
run_command "coverage run -m pytest dns"
run_command "coverage report --include 'dns/*'"
