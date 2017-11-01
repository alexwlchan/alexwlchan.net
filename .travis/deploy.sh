#!/usr/bin/env bash

set -o errexit
set -o nounset

echo "*** Loading Travis RSA key"
openssl aes-256-cbc \
  -K $encrypted_83630750896a_key \
  -iv $encrypted_83630750896a_iv \
  -in .travis/id_rsa.enc \
  -out id_rsa -d

echo "*** Uploading published site to Linode"
chmod 400 id_rsa
mv id_rsa ~/.ssh/id_rsa
make deploy

echo "*** Configuring Git"
git config --global user.name "Travis CI on behalf of Alex Chan"
git config --global user.email "travisci_git@alexwlchan.fastmail.co.uk"
git config core.sshCommand "ssh -i id_rsa"
git remote add ssh-origin git@github.com:alexwlchan/alexwlchan.net.git

echo "*** Pushing any extra commits to GitHub"
git push ssh-origin HEAD:master
