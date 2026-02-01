---
layout: post
date: 2025-02-04 08:05:17 +00:00
title: Making inventory spreadsheets for my LEGO sets
summary: Using the Rebrickable database downloads and sqlite-utils, I can quickly create spreadsheets that let me tick off the parts in each set.
tags:
  - lego
  - sqlite
card_attribution: https://pixabay.com/photos/lego-block-toys-3602218/
  ta98mori, Pixabay Content License, retrieved 4 February 2025
---

One of my recent home organisation projects has been sorting out my LEGO collection.
I have a bunch of sets which are mixed together in one messy box, and I'm trying to separate bricks back into distinct sets.
My collection is nowhere near large enough to be worth sorting by individual parts, and I hope that breaking down by set will make it all easier to manage and store.

I've been creating spreadsheets to track the parts in each set, and count them out as I find them.
I briefly hinted at this in my post about [looking at images in spreadsheets][spreadsheet_images], where I included a screenshot of one of my inventory spreadsheets:

{%
  picture
  filename="lego_spreadsheet.png"
  width="582"
  alt="Screenshot of a spreadsheet showing a list of four Lego bricks, plus a count of how many I have/need. There are images showing an illustration of the four bricks."
  class="screenshot"
%}

These spreadsheets have been invaluable – I can see exactly what pieces I need, and what pieces I'm missing.
Without them, I wouldn't even attempt this.

I'm about to pause this cleanup and work on some other things, but first I wanted to write some notes on how I'm creating these spreadsheets -- I'll probably want them again in the future.

[spreadsheet_images]: /2025/images-and-spreadsheets/



## Getting a list of parts in a set

There are various ways to get a list of parts in a LEGO set:

* Newer LEGO sets include a list of parts at the back of the printed instructions
* You can get a list from LEGO-owned website like LEGO.com or [BrickLink]
* There are community-maintained databases on sites like [Rebrickable]

I decided to use the community maintained lists from Rebrickable -- they seem very accurate in my experience, and you can [download daily snapshots][downloads] of their entire catalog database.
The latter is very powerful, because now I can load the database into my tools of choice, and slice and dice the data in fun and interesting ways.

Downloading their entire database is less than 15MB -- which is to say, two-thirds the size of just opening the LEGO.com homepage.
Bargain!

[Rebrickable]: https://rebrickable.com/
[Bricklink]: https://www.bricklink.com/v2/main.page
[downloads]: https://rebrickable.com/downloads/



## Putting Rebrickable data in a SQLite database

My tool of choice is SQLite.
I slept on this for years, but I've come to realise just how powerful and useful it can be.
A big part of what made me realise the power of SQLite is seeing Simon Willison's work with [datasette], and some of the cool things he's built on top of SQLite.

Simon also publishes a command-line tool [sqlite-utils] for manipulating SQLite databases, and that's what I've been using to create my spreadsheets.

Here's my process:

1.  Create a Python virtual environment, and install sqlite-utils:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install sqlite-utils
    ```

    At time of writing, the latest version of sqlite-utils is 3.38.

2.  Download the Rebrickable database tables I care about, uncompress them, and load them into a SQLite database:

    ```bash
    curl -O 'https://cdn.rebrickable.com/media/downloads/colors.csv.gz'
    curl -O 'https://cdn.rebrickable.com/media/downloads/parts.csv.gz'
    curl -O 'https://cdn.rebrickable.com/media/downloads/inventories.csv.gz'
    curl -O 'https://cdn.rebrickable.com/media/downloads/inventory_parts.csv.gz'

    gunzip colors.csv.gz
    gunzip parts.csv.gz
    gunzip inventories.csv.gz
    gunzip inventory_parts.csv.gz

    sqlite-utils insert lego_parts.db colors colors.csv --csv
    sqlite-utils insert lego_parts.db parts parts.csv --csv
    sqlite-utils insert lego_parts.db inventories inventories.csv --csv
    sqlite-utils insert lego_parts.db inventory_parts inventory_parts.csv --csv
    ```

    The `inventory_parts` table describes how many of each part there are in a set.
    *"Set&nbsp;S contains 10 of part&nbsp;P in colour&nbsp;C."*

    The `parts` and `colors` table contains detailed information about each part and color.

    The `inventories` table matches the official LEGO set numbers to the inventory IDs in Rebrickable's database.
    *"The set sold by LEGO as 6616-1 has ID 4159 in the inventory table."*

3.  Run a SQLite query that gets information from the different tables to tell me about all the parts in a particular set:

    ```sql
    SELECT ip.img_url, ip.quantity, ip.is_spare, c.name as color, p.name, ip.part_num
    FROM inventory_parts ip
    JOIN inventories i ON ip.inventory_id = i.id
    JOIN parts p ON ip.part_num = p.part_num
    JOIN colors c ON ip.color_id = c.id
    WHERE i.set_num = '6616-1';
    ```

    Or use sqlite-utils to export the query results as a spreadsheet:

    ```bash
    sqlite-utils lego_parts.db "
      SELECT ip.img_url, ip.quantity, ip.is_spare, c.name as color, p.name, ip.part_num
      FROM inventory_parts ip
      JOIN inventories i ON ip.inventory_id = i.id
      JOIN parts p ON ip.part_num = p.part_num
      JOIN colors c ON ip.color_id = c.id
      WHERE i.set_num = '6616-1';" --csv > 6616-1.csv
    ```

    Here are the first few lines of that CSV:

    ```
    img_url,quantity,is_spare,color,name,part_num
    https://cdn.rebrickable.com/media/parts/photos/9999/23064-9999-e6da02af-9e23-44cd-a475-16f30db9c527.jpg,1,False,[No Color/Any Color],Sticker Sheet for Set 6616-1,23064
    https://cdn.rebrickable.com/media/parts/elements/4523412.jpg,2,False,White,Flag 2 x 2 Square [Thin Clips] with Chequered Print,2335pr0019
    https://cdn.rebrickable.com/media/parts/photos/15/2335px13-15-33ae3ea3-9921-45fc-b7f0-0cd40203f749.jpg,2,False,White,Flag 2 x 2 Square [Thin Clips] with Octan Logo Print,2335pr0024
    https://cdn.rebrickable.com/media/parts/elements/4141999.jpg,4,False,Green,Tile Special 1 x 2 Grille with Bottom Groove,2412b
    https://cdn.rebrickable.com/media/parts/elements/4125254.jpg,4,False,Orange,Tile Special 1 x 2 Grille with Bottom Groove,2412b
    ```

4.  Import that spreadsheet into Google Sheets, then add a couple of columns.

    I add a column `image` where every cell has the formula `=IMAGE(…)` that references the image URL.
    This gives me an inline image, so I know what that brick looks like.

    I add a new column `quantity I have` where every cell starts at 0, which is where I'll count bricks as I find them.

    I add a new column `remaining to find` which counts the difference between `quantity` and `quantity I have`.
    Then I can highlight or filter for rows where this is non-zero, so I can see the bricks I still need to find.

    If you're interested, [here's an example spreadsheet][example] that has a clean inventory.

It took me a while to refine the SQL query, but now I have it, I can create a new spreadsheet in less than a minute.

One of the things I've realised over the last year or so is how powerful "get the data into SQLite" can be – it opens the door to all sorts of interesting queries and questions, with a relatively small amount of code required.
I'm sure I could write a custom script just for this task, but it wouldn't be as concise or flexible.

[datasette]: https://datasette.io/
[sqlite-utils]: https://sqlite-utils.datasette.io/en/stable/
[example]: https://docs.google.com/spreadsheets/d/10FzybJlLA1xyJydWM3X8KRpY0XFHkKK9Bxwdxg7DSMw/edit?usp=sharing
