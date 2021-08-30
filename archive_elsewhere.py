#!/usr/bin/env python

import os
import re
import yaml

import click
from unidecode import unidecode


ELSEWHERE_YML_PATH = "src/_data/elsewhere.yml"
ARCHIVE_DIR = "/Volumes/Media (Sapphire)/backups/alexwlchan.net/elsewhere"


def slugify(u):
    """Convert Unicode string into blog slug.

    From http://www.leancrew.com/all-this/2014/10/asciifying/
    """
    u = re.sub("[–—/:;,.]", "-", u)  # replace separating punctuation
    a = unidecode(u).lower()  # best ASCII substitutions, lowercased
    a = re.sub(r"[^a-z0-9 -]", "", a)  # delete any other characters
    a = a.replace(" ", "-")  # spaces to hyphens
    a = re.sub(r"-+", "-", a)  # condense repeated hyphens
    return a


if __name__ == "__main__":
    elsewhere = yaml.safe_load(open(ELSEWHERE_YML_PATH))

    for writing in elsewhere["writing"]:
        out_dir = os.path.join(
            ARCHIVE_DIR,
            slugify(
                writing["url"]
                .replace("https://", "")
                .replace("www.", "")
                .replace("lastweekinaws.com/blog/", "lastweekinaws/")
            ).strip("-"),
        )

        os.makedirs(out_dir, exist_ok=True)

        if os.listdir(out_dir):
            writing["archived_paths"] = [
                os.path.join(out_dir, p) for p in os.listdir(out_dir)
            ]
            continue

        print(f"URL:        {writing['url']}")
        print(f"Backup dir: {out_dir}")

        while not click.confirm("Have you saved archive copies?"):
            pass

        writing["archived_paths"] = [
            os.path.join(out_dir, p) for p in os.listdir(out_dir)
        ]

        print("")

    with open(ELSEWHERE_YML_PATH, "w") as outfile:
        yaml.dump(elsewhere, outfile)
