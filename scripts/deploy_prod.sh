#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

mkdir -p ~/.ssh
ls -l ~/.ssh
cp "$DOWNLOADSECUREFILE_SECUREFILEPATH" ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa

ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Even though Azure doesn't set anything in this file, it gets
# mounted as a container volume by "make deploy".  If it doesn't
# exist, Docker creates an empty directory and Git is unhappy.
touch ~/.gitconfig

git config user.name "Azure Pipelines on behalf of Alex Chan"
git config user.email "azurepipelines_git@alexwlchan.net"

make deploy-prod

git remote add ssh-origin git@github.com:alexwlchan/alexwlchan.net.git
git push --verbose ssh-origin HEAD:live