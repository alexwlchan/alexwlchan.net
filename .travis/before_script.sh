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
