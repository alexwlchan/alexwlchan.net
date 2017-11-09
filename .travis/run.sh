#!/usr/bin/env bash

set -o errexit
set -o nounset

banner() {
  echo "*********************************************************************"
  echo "$1 [$(date)]"
  echo "*********************************************************************"
}


# Start the site build in the background.  This usually takes 20-30 seconds,
# so while it's running we can get on with some other tasks.
banner "Starting the development server"
make serve

# At this point, the server is the only containing running.
docker_id=$(docker ps -q)


# We run this while we wait for the server to be ready.
banner "Running check-format task"
make check-format

# We also prepare the test container at this point.
banner "Building test container"
make .docker/tests


banner "Finished other tasks, waiting for server to become available..."
set +o errexit
while true
do
    curl 'http://localhost:5757' >/dev/null 2>&1
    if (( $? == 0 ))
    then
        break
    fi
    echo "Still waiting for server to become available..."
    sleep 2

    # If the container has died, give up
    docker ps | grep "$docker_id" >/dev/null 2>&1
    if (( $? != 0 ))
    then
        banner "Unexpected failure!"
        echo "'make serve' task has unexpectedly failed; giving up"
        echo "Container logs:"
        echo "==="
        docker logs $docker_id
        echo "==="
        exit 2
    fi
done
set -o errexit

banner "Running the server tests"
make test

if [[ "$TRAVIS_EVENT_TYPE" == "pull_request" ]]
then
  banner "Pull request, skipping deploy to prod"
  exit 0
fi

.travis/deploy.sh
