#!/usr/bin/env bash
# This script installs ImageMagick 7.
#
# This is required for supporting AVIF images with transparency; the version
# of ImageMagick available from `apt-get install` is only 6.9, which replaces
# transparency backgrounds with all black.

set -o errexit
set -o nounset
set -o verbose

apt-get update

# This runs a tool called IMEI (ImageMagick Easy Install), which includes
# fetching all the dependencies and running the build commands.
apt-get install --yes wget
wget 'https://dist.1-2.dev/imei.sh'
bash imei.sh --skip-jxl

# This removes a bunch of dependencies that are needed for building and
# installing ImageMagick, but which aren't required to run it.
#
# This helps keep the size of the final Docker image down.
apt-get remove --yes \
  autoconf \
  autotools-dev \
  cmake \
  cpp \
  curl \
  gcc \
  git \
  jq \
  libicu-dev \
  libllvm11 \
  libssl-dev \
  libx265-dev \
  make \
  openssh-client \
  openssl \
  perl \
  python3 \
  unzip \
  wget \
  zlib1g-dev

apt autoremove --yes

# Print the ImageMagick version, and confirm we haven't pruned too far.
convert -version
