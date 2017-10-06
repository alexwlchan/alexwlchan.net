#!/usr/bin/env bash

set -o errexit
set -o nounset

# Ensure that Docker layers are cached between Travis runs.  This is based on:
# https://gist.github.com/hc2p/9e284cee3d585eefbc59454e44cc247a

sudo service docker stop

if [[ "$(ls -A /home/travis/docker)" ]]
then
	echo "/home/travis/docker already set"
else
	sudo mv /var/lib/docker /home/travis/docker
fi

sudo bash -c "echo 'DOCKER_OPTS=\"-H tcp://127.0.0.1:2375 -H unix:///var/run/docker.sock -g /home/travis/docker\"' > /etc/default/docker"
sudo service docker start

# Set up Git config.  This is required for the 'publish-drafts' task.
git config user.name "Travis CI on behalf of Alex Chan"
git config user.email "travisci_git@alexwlchan.fastmail.co.uk"
git remote rm origin
git remote add origin git@github.com:alexwlchan/alexwlchan.net.git

# See https://github.com/travis-ci/travis-ci/issues/6652.  A no-op that sets
# the current branch and establishes the upstream.
BRANCH="${TRAVIS_PULL_REQUEST_BRANCH:-$TRAVIS_BRANCH}"
git checkout -b "$BRANCH"
git push --set-upstream origin "$BRANCH"
