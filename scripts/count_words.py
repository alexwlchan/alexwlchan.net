#!/usr/bin/env python3
"""
Count the number of words I've published each year.
"""

import collections
from pathlib import Path
import sys

import termcolor

sys.path.append(str(Path(__file__).parent.parent))

from mosaic import Site
from mosaic.html_page import Article


def count_words(content: str) -> int:
    """
    Count the words in a block of Markdown.
    """
    # Remove all the blockquotes from the content
    content = "\n".join(
        ln.strip() for ln in content.splitlines() if not ln.strip().startswith("> ")
    )

    word_count = 0
    in_block_statement = 0

    for char_sequence in content.split():
        if char_sequence in {
            "-",
            "--",
            "---",
            "–",
            "{",
            "}",
            "=",
            "*",
            "#",
            "##",
            "###",
            "####",
            "#####",
        }:
            continue

        if char_sequence.startswith("```"):
            continue

        if char_sequence in {"{%", "<svg", "<picture"}:
            in_block_statement += 1
            continue
        elif char_sequence in {"%}", "</svg>", "</picture>"}:
            in_block_statement -= 1
            continue

        if in_block_statement == 0:
            word_count += 1

    return word_count


if __name__ == "__main__":
    site = Site()
    pages = site.read_markdown_source_files()

    articles_tally: dict[int, list[int]] = collections.defaultdict(list)
    remaining_tally: dict[int, list[int]] = collections.defaultdict(list)

    for p in pages:
        if p.date is None:
            continue

        if isinstance(p, Article):
            articles_tally[p.date.year].append(count_words(p.content))
        else:
            remaining_tally[p.date.year].append(count_words(p.content))

    print("       articles   others    total")
    print("====== ======== ======== ========")

    for year in sorted(articles_tally):
        print(
            f"{year}\t"
            f"{sum(articles_tally[year]):7,}\t "
            f"{sum(remaining_tally[year]):7,}  "
            f"{sum(articles_tally[year] + remaining_tally[year]):7,}"
        )

    articles_total = sum(sum(wc) for wc in articles_tally.values())
    remaining_total = sum(sum(wc) for wc in remaining_tally.values())

    print("====== ======== ======== ========")
    print(
    termcolor.colored(
        f"TOTAL\t"
        f"{articles_total:7,}\t "
        f"{remaining_total:7,}  "
        f"{articles_total + remaining_total:7,}", 'blue')
    )
