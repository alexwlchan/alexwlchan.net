---
layout: til
title: "Installing mimetype on Alpine Linux"
date: 2019-08-28 13:49:55 +01:00
tags:
  - alpine
---

I needed to install [mimetype(1)] in Alpine because it's used by the [preview-generator] library.

```console
$ docker run -it alpine sh

# apk add apkbuild-cpan build-base perl perl-dev shared-mime-info
# PERL_MM_USE_DEFAULT=1 cpan File::BaseDir
# PERL_MM_USE_DEFAULT=1 cpan File::MimeInfo
# apk del apkbuild-cpan build-base perl-dev

# echo "# README" > README.md
# mimetype README.md
README.md: text/markdown
```

[mimetype(1)]: https://linux.die.net/man/1/mimetype
[preview-generator]: https://pypi.org/project/preview-generator/
