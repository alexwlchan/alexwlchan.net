#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o verbose

apt-get update

# These packages are both necessary to install Jekyll
apt-get install --yes build-essential zlib1g-dev

# Required for the static file plugin
apt-get install --yes rsync

# Required for the publish-drafts plugin
apt-get install --yes git

# Required for the rszr gem, which I use for pictures and the Twitter plugin
# See https://github.com/mtgrosser/rszr#debian-based
apt-get install --yes libimlib2 libimlib2-dev

# Required to inspect colour profiles in the image linting plugin
apt-get install --yes exiftool

# Required to create differently sized images for WebP/AVIF
# Theoretically I could use `rszr` like in the Twitter plugin, but it
# doesn't support AVIF.
#
# Note: temporarily disabled until Debian has ImageMagick 7 available
# from `apt-get`.  I'm building my own version from source so that
# transparency works with AVIF.
#
# apt-get install --yes imagemagick

# Required by the http-proofer gem, which is used by the linter plugin.
# Without it, I get an error:
#
#     Could not open library 'libcurl.so.4': libcurl.so.4
#
# I tried `apt-get install libcurl-dev` and was offered three options:
#
#     Package libcurl-dev is a virtual package provided by:
#       libcurl4-openssl-dev 7.74.0-1.3+deb11u3
#       libcurl4-nss-dev 7.74.0-1.3+deb11u3
#       libcurl4-gnutls-dev 7.74.0-1.3+deb11u3
#     You should explicitly select one to install.
#
# I don't know what the different between them is, so I picked arbitrarily.
apt-get install --yes libcurl4-gnutls-dev

# Actually install the Ruby gems!
bundle install

# These packages are only required for installation, and I can remove them
# from the final image.
apt-get remove --yes build-essential zlib1g-dev
apt autoremove --yes
