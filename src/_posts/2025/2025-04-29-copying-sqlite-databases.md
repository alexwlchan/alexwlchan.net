---
layout: post
date: 2025-04-29 21:47:09 +00:00
title: A faster way to copy SQLite databases between computers
summary:
  Dumping a SQLite database to a text file can make it much smaller, which means you can download it faster.
tags:
  - sqlite
---
I store a lot of data in SQLite databases on remote servers, and I often want to copy them to my local machine for analysis or backup.

When I'm starting a new project and the database is near-empty, this is a simple rsync operation:

```console
$ rsync --progress username@server:my_remote_database.db my_local_database.db
```

As the project matures and the database grows, this gets slower and less reliable.
Downloading a 250MB database from my web server takes about a minute over my home Internet connection, and that's pretty small -- most of my databases are multiple gigabytes in size.

I've been trying to make these copies go faster, and I recently discovered a neat trick.

What really slows me down is my indexes.
I have a lot of indexes in my SQLite databases, which dramatically speed up my queries, but also make the database file larger and slower to copy.
(In one database, there's an index which single-handedly accounts for half the size on disk!)

The indexes don't store anything unique -- they just duplicate data from other tables to make queries faster.
Copying the indexes makes the transfer less efficient, because I'm copying the same data multiple times.
I was thinking about ways to skip copying the indexes, and I realised that SQLite has built-in tools to make this easy.

## Dumping a database as a text file

SQLite allows you to [dump a database as a text file][dump].
If you use the `.dump` command, it prints the entire database as a series of SQL statements.
This text file can often be significantly smaller than the original database.

Here's the command:

```console
$ sqlite3 my_database.db .dump > my_database.db.txt
```

And here's what the beginning of that file looks like:

```sql
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "tags" (
   [name] TEXT PRIMARY KEY,
   [count_uses] INTEGER NOT NULL
);
INSERT INTO tags VALUES('carving',260);
INSERT INTO tags VALUES('grass',743);
…
```

Crucially, this reduces the large and disk-heavy indexes into a single line of text -- it's an instruction to create an index, not the index itself.

```sql
CREATE INDEX [idx_photo_locations]
    ON [photos] ([longitude], [latitude]);
```

This means that I'm only storing each value once, rather than the many times it may be stored across the original table and my indexes.
This is how the text file can be smaller than the original database.

If you want to reconstruct the database, you pipe this text file back to SQLite:

```console
$ cat my_database.db.txt | sqlite3 my_reconstructed_database.db
```

Because the SQL statements are very repetitive, this text responds well to compression:

```console
$ sqlite3 explorer.db .dump | gzip -c > explorer.db.txt.gz
```

To give you an idea of the potential savings, here's the relative disk size for one of my databases.

<style>
  table#sizes {
    width: 100%;
    border: var(--border-width) var(--border-style) var(--block-border-color);
    border-radius: var(--border-radius);
    background-color: var(--block-background);
    padding: var(--default-padding);
  }

  table#sizes tr:not(:last-of-type) > th,
  table#sizes tr:not(:last-of-type) > td {
    border-bottom: 2px solid var(--block-border-color);
  }

  table#sizes td:not(:first-child) {
    text-align: center;
  }

  table#sizes tr > td:nth-child(2) {
    padding-left: 1em;
  }
</style>

<table id="sizes">
  <tr>
    <th>File</th>
    <th>Size on disk</th>
  </tr>
  <tr>
    <td>original SQLite database</td>
    <td title="7,081,912 bytes">3.4 GB</td>
  </tr>
  <tr>
    <td>text file (<code>sqlite3 my_database.db .dump</code>)</td>
    <td title="2,785,408 bytes">1.3 GB</td>
  </tr>
  <tr>
    <td>gzip-compressed text (<code>sqlite3 my_database.db .dump | gzip -c</code>)</td>
    <td title="491,904 bytes">240 MB</td>
  </tr>
</table>

The gzip-compressed text file is 14× smaller than the original SQLite database -- that makes downloading the database much faster.

[dump]: https://sqlite.org/cli.html#converting_an_entire_database_to_a_text_file

## My new ssh+rsync command

Rather than copying the database directly, now I create a gzip-compressed text file on the server, copy that to my local machine, and reconstruct the database.
Like so:

```shell
# Create a gzip-compressed text file on the server
ssh username@server "sqlite3 my_remote_database.db .dump | gzip -c > my_remote_database.db.txt.gz"

# Copy the gzip-compressed text file to my local machine
rsync --progress username@server:my_remote_database.db.txt.gz my_local_database.db.txt.gz

# Remove the gzip-compressed text file from my server
ssh username@server "rm my_remote_database.db.txt.gz"

# Uncompress the text file
gunzip my_local_database.db.txt.gz

# Reconstruct the database from the text file
cat my_local_database.db.txt | sqlite3 my_local_database.db

# Remove the local text file
rm my_local_database.db.txt
```



## A database dump is a stable copy source

This approach fixes another issue I've had when copying SQLite databases.

If it takes a long time to copy a database and it gets updated midway through, rsync may give me an invalid database file.
The first half of the file is pre-update, the second half file is post-update, and they don't match.
When I try to open the database locally, I get an error:

```
database disk image is malformed
```

By creating a text dump before I start the copy operation, I'm giving rsync a stable copy source.
That text dump isn't going to change midway through the copy, so I'll always get a complete and consistent text file.

---

This approach has saved me hours when working with large databases, and made my downloads both faster and more reliable.
If you have to copy around large SQLite databases, give it a try.
