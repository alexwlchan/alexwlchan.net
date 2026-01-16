---
layout: til
title: Running the Netlify CLI in GitHub Actions
date: 2024-01-06 10:05:00 +00:00
tags:
  - netlify
  - github actions
---
Currently I run Netlify using [a Docker image provided by William Jackson](https://github.com/williamjacksn/docker-netlify-cli).
This has worked well for a while, but occasionally something breaks when Netlify bumps their CLI version.

While looking around for how other people solve this, I found [a set of GitHub Actions published by Netlify](https://github.com/netlify/actions), which includes a CLI Action – however, there have been no commits for two years, and there's a stack of unhandled issues and pull requests.
It's unclear if Netlify still cares about it.

Additionally, I got several deprecation warnings when I tried running it in one of my repositories:

```
Warning: The `set-output` command is deprecated and will be disabled soon. Please upgrade to using Environment Files. For more information see: https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
Warning: The `set-output` command is deprecated and will be disabled soon. Please upgrade to using Environment Files. For more information see: https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
https://app.netlify.com/sites/books-alexwlchan/functions
Warning: The `set-output` command is deprecated and will be disabled soon. Please upgrade to using Environment Files. For more information see: https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
```

I haven't looked at how much work it would be to get it up-to-date with modern GitHub Actions, but for now I'm going to keep using the third-party image.
