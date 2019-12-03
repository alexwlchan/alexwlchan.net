#!/usr/bin/env python
# -*- encoding: utf-8

import os
import pathlib

import frontmatter
import iterfzf


def get_post_paths(root):
    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if f.endswith(".md"):
                yield pathlib.Path(dirpath) / f


def get_posts(root):
    for path in get_post_paths(root):
        yield (path, frontmatter.load(open(path)))


if __name__ == "__main__":
    posts = {}

    for path, front_matter in get_posts(root="src/_posts"):
        posts[front_matter["title"]] = {
            "path": path,
            "front_matter": front_matter
        }

    titles = sorted(
        posts.keys(),
        key=lambda p: posts[p]["front_matter"]["date"],
        reverse=True
    )
    selected_title = iterfzf.iterfzf(titles, multi=False)
    post = posts[selected_title]

    category = post["front_matter"].get("category")

    categories = {
        p["front_matter"].get("category")
        for p in posts.values()
        if p["front_matter"].get("category")
    }

    new_category = iterfzf.iterfzf(sorted(categories))

    post["front_matter"]["category"] = new_category

    with open(post["path"], "wb") as outfile:
        frontmatter.dump(post["front_matter"], outfile)

    if category:
        print(f"{post['front_matter']['title']}: updating category from {category} to {new_category}")
    else:
        print(f"{post['front_matter']['title']}: adding category {new_category}")
