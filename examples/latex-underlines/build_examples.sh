#!/usr/bin/env sh

set -o errexit
set -o nounset

OUTDIR="output"
mkdir -p "$OUTDIR"

for f in example_*.tex
do
  echo "*** Processing $f"
  name="$(basename $f)"
  pdflatex -output-directory="$OUTDIR" "$f"
  pdftoppm "$OUTDIR/${name/tex/pdf}" -png -f 1 -singlefile -rx 600 -ry 600 "$OUTDIR/${name/.tex/}"
  optipng "$OUTDIR/${name/tex/png}"
done

find "$OUTDIR" -depth 1 -not -name "*.png" -delete
