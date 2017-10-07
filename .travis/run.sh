#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Starting the development server"
make serve

docker_id=$(docker ps -q)

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

echo "*** Uploading published site to Linode"
openssl aes-256-cbc -K $encrypted_83630750896a_key -iv $encrypted_83630750896a_iv -in .travis/id_rsa.enc -out id_rsa_travis -d
chmod 400 id_rsa_travis
export SSHOPTS=" -o StrictHostKeyChecking=no -i id_rsa_travis"
make publish

# Set up Git config.
git config user.name "Travis CI on behalf of Alex Chan"
git config user.email "travisci_git@alexwlchan.fastmail.co.uk"
git remote rm origin
git remote add ssh-origin git@github.com:alexwlchan/alexwlchan.net.git

# Set up the SSH key that allows Travis to push to GitHub
openssl aes-256-cbc -K $encrypted_83630750896a_key -iv $encrypted_83630750896a_iv -in .travis/id_rsa_push_key.enc -out id_rsa_push_key -d
md5sum id_rsa_push_key
chmod 600 id_rsa_push_key
ssh-agent sh -c "chmod 600 id_rsa_push_key && ssh-add id_rsa_push_key && git push ssh-origin HEAD:publish-drafts"
