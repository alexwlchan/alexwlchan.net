---
layout: til
title: What secrets do I have configured in GitHub Actions?
date: 2025-04-28 12:03:01 +0100
tags:
  - github actions
---
```bash
gh repo list alexwlchan \
    --limit 1000 \
    --json owner,name \
    --jq '.[] | "\(.owner.login)/\(.name)"' \
  | xargs -I '{}' sh -c "echo '\n{}'; gh secret list --repo '{}'"
```