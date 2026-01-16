---
layout: til
title: How to suppress installing rdoc/ri docs when running `gem install`
date: 2018-11-26 10:13:25 +00:00
tags:
  - ruby
  - docker
---

If you try to run `gem install` in a Docker container which only contains a Ruby package (and no rdoc or ri), you get an error:

```
Step 3/5 : RUN gem install rack
 ---> Running in 8ee24453f7a9
ERROR:  While executing gem ... (Gem::DocumentError)
    RDoc is not installed: cannot load such file -- rdoc/rdoc
```

If you add the following line to your `.gemrc`, it skips trying to install the docs.

```
install: --no-rdoc --no-ri
```

Handy if you're in a Docker image that will never run interactively!
