#!/usr/bin/env bash

set -o errexit
set -o nounset

convert -background none -flatten -colors 256 favicon-16x16.png favicon-16x16.ico
convert -background none -flatten -colors 256 favicon-32x32.png favicon-32x32.ico
convert favicon-16x16.ico favicon-32x32.ico favicon.ico
