#!/usr/bin/env bash

set -o errexit
set -o nounset

# Print a command in blue, then run the command
run_command() {
    echo ""
    echo -e "\033[34m-> $@\033[0m"
    bash -c "$@"
}

run_command 'rm -vf .mosaic_cache.db'
run_command 'python3 scripts/build_site.py'
run_command 'rsync --compress --recursive --delete --verbose --checksum --exclude=.DS_Store --exclude=my-tools/library-lookup/ _out/ linode-vps:repos/alexwlchan.net/_site/'
