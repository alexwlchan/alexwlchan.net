#!/usr/bin/env bash
# Use an image as a card for one of my posts.
#
# Call this script with a link to an image anywhere on disk,
# and it will:
#
#   * Convert the image to an sRGB colour profile
#   * Move the image into the appropriate folder in "src"
#   * Purge any cached card data from the "_site" folder
#

set -o errexit
set -o nounset

CARD_PATH="$1"

ROOT="$(git rev-parse --show-toplevel)"
YEAR=$(date "+%Y")

CARD_DIR="$ROOT/src/_images/cards/$YEAR"
mkdir -p "$CARD_DIR"

source ~/repos/scripts/.venv/bin/activate
python3 ~/repos/scripts/images/srgbify.py "$CARD_PATH" >/dev/null

CARD_FILENAME="$(basename "$CARD_PATH")"

# When Keynote exports a JPEG file, it uses ".jpeg" as the
# extension but I want the ".jpg" extension in my filenames.
if [[ "$CARD_FILENAME" == *.jpeg ]]; then
    CARD_FILENAME="${CARD_FILENAME%.jpeg}.jpg"
fi

# When Keynote exports a deck of slides, it includes the
# slide number in the filename, e.g. "myslide.001.jpeg"
#
# Remove the slide number.
CARD_FILENAME=$(echo "$CARD_FILENAME" | sed -E 's/\.[0-9]{3}//')

# Move the image into the current "cards" directory
mv "$CARD_PATH" "$CARD_DIR/$CARD_FILENAME"

# Purge any existing cards
CARD_FILENAME_WITHOUT_SUFFIX="${CARD_FILENAME%.*}"

find "$ROOT/_site" -name "$CARD_FILENAME_WITHOUT_SUFFIX*" -delete
