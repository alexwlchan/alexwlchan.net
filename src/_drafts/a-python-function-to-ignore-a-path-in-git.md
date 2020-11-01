---
layout: post
title: A Python function to ignore a path in Git
summary: If your Python script creates a file that you don't want to track in Git, here's how you can ignore it.
tags: git python
---

One of the things I work on is [a Catalogue API](https://developers.wellcomecollection.org/catalogue) for searching Wellcome Collection's collections.
The API returns "works", and a work can include metadata and images -- for example, the individual pages of a digitised book.
Sometimes I need all the images from a work, so I wrote [a Python script](https://github.com/wellcomecollection/catalogue/pull/999) that uses the API to find all the images, then download them to a local directory.

Like all our code, this script lives in a Git repo, and it saves images to the working directory -- usually the folder with the script in.
This means the images it saves are visible to Git, and the next time I run `git status`, it'll offer to track the images alongside our code.
That's not what I want -- these images are temporary downloads, not part of our codebase.

I could remember not to check in these images, and delete them when I'm done -- but they clutter up my Git tooling, and I could make a mistake.

I could add the images to `.gitignore`, but that gets tracked as part of the codebase.
Nobody else needs to be ignoring these paths, because they haven't downloaded these images.

I could save the images in a different directory, but that's slightly less convenient.

**I realised this was a good use case [for `.git/info/exclude`](/2015/06/git-info-exclude/) -- a place for gitignore rules that shouldn't tracked as part of the repo history.**
Each clone can have different rules in this file.
If I ignore the downloaded images in this file, they won't show up in `git status`, but nor will the ignore rules be shared with anyone else.

I could add images to `.git/info/exclude` by hand, but I'm already running a script, so I extended the script to ignore these files automatically.
I wrote a Python function that appends a path to `.git/info/exclude`:

```python
import os
import subprocess


def ignore_path_locally(path):
    """
    Tell Git to ignore a path, but without adding it to the .gitignore.

    This function instead adds paths to .git/info/exclude.

    See https://alexwlchan.net/2015/06/git-info-exclude/
    """
    # Get the absolute path to the root of the repo.
    # See https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---show-toplevel
    repo_root = subprocess.check_output([
        "git", "rev-parse", "--show-toplevel"]).strip().decode("utf8")

    # Get the path of the file/directory to ignore, relative to the root
    # of the repo.
    path_to_ignore = os.path.relpath(path, start=repo_root)

    # Gets the path to info/exclude inside the .git directory.
    # See https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---git-pathltpathgt
    git_info_exclude_path = subprocess.check_output(
        ["git", "rev-parse", "--git-path", "info/exclude"]).strip().decode("utf8")

    with open(git_info_exclude_path, "a") as exclude_file:
        exclude_file.write(path_to_ignore + "\n")
```

Inside the script, I call this function to add downloaded paths to `.git/info/exclude`.

Hopefully the comments mean you can see how this function works.
There are a couple of Git features it's using that are worth highlighting:

*   **If you want to get the root of a repo, use [`git rev-parse --show-toplevel`](https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---show-toplevel).**

    You can run this anywhere inside a Git repo, and it tells you the top-level directory.
    I find this particularly useful in build scripts.

*   **If you want to find the `.git` directory, use [`git rev-parse --git-dir`](https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---git-dir).**

    **If you want a path inside the `.git` directory, use [`git rev-parse --git-path <PATH>`](https://git-scm.com/docs/git-rev-parse#Documentation/git-rev-parse.txt---git-pathltpathgt).**

    Normally the `.git` directory lives directly under the root of a repo, but it's possible for it to live elsewhere (and its location specified with the [`$GIT_DIR` environment variable](https://git-scm.com/book/en/v2/Git-Internals-Environment-Variables#_repository_locations)).
    Using `rev-parse` to find it, and resolve paths inside it, is more robust than guessing the location in your code.

    This is a classic example of something I learnt while writing a blog post.
    I went to check the definition for `git-rev-parse --show-toplevel`, and while on the page I spotted the `--git-dir` flag.
    That was the first time I realised the `.git` directory could move around, and then I found `--git-path` while editing the post.
    Blog posts are as much about what I can learn as what I can teach other people.

*   **Paths in a gitignore or exclude file should be relative to the root of a repo.**

    Suppose I have a repo at `/home/alex/myrepo`, and inside that repo I have a file `code/localoutput.txt` that I want to ignore.
    In my gitignore or exclude file, I need to put the path relative to the root of the repo, that is:

    ```
    👎 /home/alex/myrepo/code/localoutput.txt
    👍 code/localoutput.txt
    ```

    Although absolute paths are often preferable for disambiguity, in Git's case they cause issues.
    If my coworker checks out this repo on her computer, the absolute path to this file might be `/home/alice/myrepo/code/localoutput.txt`, and the absolute path from my machine is no good to her.

    The function above will handle this, but I got it wrong in my first attempt.
