The favicon templates were generated by running:

```console
convert -background none -flatten favicon-16x16.svg template-16x16.png
convert -background none -flatten favicon-32x32.svg template-32x32.png
```

with ImageMagick inside an Alpine container.

The exact spacing seems to vary a bit, possibly depending on the fonts you use?
In particular it looks different if I run it on macOS.

I don't expect to regenerate these very often; I'm recording this mostly for posterity.

