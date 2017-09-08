#!/usr/bin/env bash

set -o errexit
set -o nounset

# Start serving the site in the background
trap make stop exit
echo "*** Starting the development server"
make serve

# Wait for the server to become available
set +o errexit
while true
do
    curl 'http://localhost:5757' >/dev/null 2>&1
    if (( $? == 0 ))
    then
        break
    fi
    echo "Waiting for server to become available..."
    sleep 2

    # If the container has died, give up
    docker ps | grep alexwlchan.net_serve >/dev/null 2>&1
    if (( $? != 0 ))
    then
        echo "'make serve' task has unexpectedly failed; giving up"
        exit 2
    fi
done
set -o errexit

sleep 40

echo "*** Running the server tests"
py.test _tests
