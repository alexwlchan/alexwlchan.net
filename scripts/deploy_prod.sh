#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

chmod 600 "$DOWNLOADSECUREFILE_SECUREFILEPATH"
git config core.sshCommand "ssh -i $DOWNLOADSECUREFILE_SECUREFILEPATH -F /dev/null"

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