#!/usr/bin/env python3
"""
Count the number of words I've published each year.
"""

import collections
from pathlib import Path
import sys


sys.path.append(str(Path(__file__).parent.parent))

from mosaic.page_types import Article, read_markdown_files
from mosaic.text import coloured


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
    pages = read_markdown_files(src_dir=Path("src"))

    articles_tally: dict[int, list[int]] = collections.defaultdict(list)
    remaining_tally: dict[int, list[int]] = collections.defaultdict(list)

    for p in pages:
        if p.date is None:
            continue

        if isinstance(p, Article):
            articles_tally[p.date.year].append(count_words(p.content))
        else:
            remaining_tally[p.date.year].append(count_words(p.content))

    print("           articles          others            total")
    print("======  ===============  ===============  ================")

    for year in sorted(articles_tally):
        articles_wc_year = sum(articles_tally[year])
        remaining_wc_year = sum(remaining_tally[year])
        total_wc_year = articles_wc_year + remaining_wc_year

        articles_count_year = len(articles_tally[year])
        remaining_count_year = len(remaining_tally[year])
        total_count_year = articles_count_year + remaining_count_year

        print(
            f"{year}     "
            f"{articles_wc_year:7,} / {articles_count_year:3}    "
            f"{remaining_wc_year:7,} / {remaining_count_year:3}    "
            f"{total_wc_year:7,} / {total_count_year:4}"
        )

    articles_wc = sum(sum(wc) for wc in articles_tally.values())
    remaining_wc = sum(sum(wc) for wc in remaining_tally.values())
    total_wc = articles_wc + remaining_wc

    articles_count = sum(len(wc) for wc in articles_tally.values())
    remaining_count = sum(len(wc) for wc in remaining_tally.values())
    total_count = articles_count + remaining_count

    print("======  ===============  ===============  ================")
    print(
        coloured(
            f"TOTAL    "
            f"{articles_wc:7,} / {articles_count:3}    "
            f"{remaining_wc:7,} / {remaining_count:3}    "
            f"{total_wc:7,} / {total_count:4}",
            "blue",
        )
    )
