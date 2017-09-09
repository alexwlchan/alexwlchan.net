#!/usr/bin/env bash

set -o errexit
set -o nounset

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

echo "*** Stopping the server, producing a release build"
docker stop alexwlchan.net_serve
make publish

echo "*** Uploading published site to Linode"
openssl aes-256-cbc -K $encrypted_83630750896a_key -iv $encrypted_83630750896a_iv -in id_rsa_travis.enc -out id_rsa_travis -d
chmod 400 id_rsa_travis
rsync \
  --archive \
  --verbose \
  --compress \
  --delete \
  --rsh="ssh -o StrictHostKeyChecking=no -i id_rsa_travis" \
  _site "$RSYNC_USER"@"$RSYNC_HOST":"$RSYNC_DIR"
