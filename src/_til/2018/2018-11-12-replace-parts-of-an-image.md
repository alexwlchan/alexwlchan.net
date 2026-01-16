---
layout: til
title: "Replace black/white parts of an image with ImageMagick"
date: 2018-11-12 09:09:23 +00:00
tags:
  - imagemagick
---

Replace white sections of an image with transparency:

```console
$ convert myimage.jpg -transparent white myimage.png
```

If it's not pure white, and you need a bit of extra:

```console
$ convert myimage.jpg -fuzz 10% -transparent white myimage.png
```

If you want to additionally crop the image to the nontransparent portion:

```console
$ convert myimage.jpg -fuzz 10% -transparent white -trim myimage.png
```

---

