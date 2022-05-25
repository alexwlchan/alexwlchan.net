#!/usr/bin/env python3

import os


def get_pull_request_number():
    # GITHUB_REF is the tag ref that triggered the workflow run,
    # which for pull requests looks something like 'refs/pull/496/merge'.
    github_ref = os.environ['GITHUB_REF']
    parts = github_ref.split('/')

    if parts[1] != 'pull':
        raise RuntimeError(f'$GITHUB_REF={GITHUB_REF}; is this a pull request build?')

    return parts[2]


if __name__ == '__main__':
    pr_number = get_pull_request_number()
    print(f"Deduced pull request as https://github.com/alexwlchan/alexwlchan.net/pull/{pr_number}")