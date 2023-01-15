#!/usr/bin/env python3

import os

for line in open('paths.txt'):
    os.unlink(line)