---
layout: til
title: How to install an asset from a GitHub release
date: 2024-11-22 11:35:50 +0000
tags:
  - github
  - github actions
summary:
  Use `gh release download`, which includes a pattern matcher if you want to pick a specific asset.
---
I wanted to install Caddy in GitHub Actions, and one of the ways [to install it](https://caddyserver.com/docs/install#static-binaries) is by downloading static binaries from their GitHub releases.

I wasn't sure how to download release assets in a sensible way -- I've written shell scripts for it before, but it feels messy and fragile.
Surely there must be a better way!

I stumbled upon [a GitHub Action](https://github.com/php/php-src/blob/master/.github/actions/setup-caddy/action.yml) in the PHP repository (!) which pointed me in the right direction:

```shell
gh release -R caddyserver/caddy download --pattern 'caddy_*_linux_amd64.tar.gz' -O - | sudo tar -xz -C /usr/bin caddy
sudo chmod +x /usr/bin/caddy
```

This is using [the GitHub CLI](https://cli.github.com/), which I haven't used before -- but it's pre-installed in GitHub Actions, which is very convenient for my purposes!

## In a GitHub Action

Here's how I packaged this as a step in a GitHub Action:

```yml
- name: Install Caddy
  env:
    GH_TOKEN: {% raw %}${{ github.token }}{% endraw %}
  run: |
    gh release download \
      --repo caddyserver/caddy \
      --pattern 'caddy_*_linux_amd64.tar.gz' \
      --output caddy.tar.gz
    tar -xzf caddy.tar.gz --directory /usr/local/bin
    chmod +x /usr/local/bin/caddy
    which caddy
```

It's a bit more verbose and leaves a `caddy.tar.gz` file lying around, but I find this version easier to understand and debug.

## Notes

*   You can specific a release to `gh release download`, or if not it will pick the latest release.
    If you let it pick automatically, it skips pre-releases.
