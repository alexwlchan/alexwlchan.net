---
layout: til
title: "Add a Git co-author credit with “Co-authored-by” in your commit message"
date: 2019-05-09 08:54:03 +0100
tags:
  - git
  - github
---

If you add the following lines to your commit message, the GitHub UI will show them as co-authors:

```
Co-authored-by: your name <your git email>
Co-authored-by: your co-author <their email>
```

I have a `;co` snippet for this.

References:

*   [Indu Alagarsamy's tweet where I saw this](https://twitter.com/Indu_alagarsamy/status/1125641581904551936)
*   [The GitHub blog post about the feature](https://github.blog/2018-01-29-commit-together-with-co-authors/)
