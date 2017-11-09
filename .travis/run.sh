#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Starting the development server"
make serve

docker_id=$(docker ps -q)

# Run the formatting tasks while we wait for the server to come up
make check-format

make .docker/tests

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
    docker ps | grep "$docker_id" >/dev/null 2>&1
    if (( $? != 0 ))
    then
        echo "'make serve' task has unexpectedly failed; giving up"
        echo "Container logs:"
        echo "==="
        docker logs $docker_id
        echo "==="
        exit 2
    fi
done
set -o errexit

echo "*** Running the server tests"
make test

if [[ "$TRAVIS_EVENT_TYPE" == "pull_request" ]]
then
  echo "*** Pull request, skipping deploy to prod"
  exit 0
fi

.travis/deploy.sh
