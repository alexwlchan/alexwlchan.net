---
layout: til
title: How to install exiftool in GitHub Actions
date: 2025-03-30 23:02:55 +01:00
tags:
  - swift
---
I wanted to run some tests in GitHub Actions that used [exiftool](https://exiftool.org).

It took me a few tries to install exiftool on Ubuntu (first I used `apt install`, then I forgot `sudo`), so here's a minimal working workflow for both Ubuntu and macOS:

```yml
name: Install exiftool

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  install_exiftool_ubuntu:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Install exiftool
      run: |
        sudo apt-get update
        sudo apt-get install exiftool

    - name: Run exiftool
      run: |
        # Download the logo from the exiftool homepage, then read
        # all the EXIF metadata
        curl -O "https://exiftool.org/ET-256.png"
        exiftool ET-256.png

  install_exiftool_macos:
    runs-on: macos-latest

    steps:
    - uses: actions/checkout@v4

    - name: Install exiftool
      run: brew install exiftool

    - name: Run exiftool
      run: |
        # Download the logo from the exiftool homepage, then read
        # all the EXIF metadata
        curl -O "https://exiftool.org/ET-256.png"
        exiftool ET-256.png
```