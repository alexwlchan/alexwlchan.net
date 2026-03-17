---
layout: note
date: 2026-03-17 21:36:32 +00:00
title: What's the `main` prefix in SQLite queries?
summary: SQLite uses schema prefixes like `main` and `temp` to disambiguate between attached databases and connection-specific temporary tables.
topic: SQLite
---

I was reading the SQLite database queries in the Tailscale source code today, and tables are referred to inconsistently: the schema creates tables like `CREATE TABLE main.TKAChonk`, but then queries may use `TKAChonk` or `main.TKAChonk`.
What's the difference?

I asked about it in Slack, and [Michael][mjf] and [Brad][bradfitz] explained what's going on: it's possible to attach multiple databases in SQLite, and the `main` prefix tells SQLite to look in the main database.
We only attach one database so the two references are equivalent, but in the past there used to be separate databases and it was useful to disambiguate.

Here's the relevant part of the [SQLite docs][sqlite-lang-naming]:

> In SQLite, a database object (a table, index, trigger or view) is identified by the name of the object and the name of the database that it resides in. […]
>
> If no database is specified as part of the object reference, then SQLite searches the main, temp and all attached databases for an object with a matching name. The temp database is searched first, followed by the main database, followed by all attached databases in the order that they were attached. […]
>
> If a schema name is specified as part of an object reference, it must be either "main", or "temp" or the schema-name of an attached database.

The temp database referred to here is [a set of tables][sqlite-temp-tables] created using `CREATE TEMP TABLE` which are only visible to the database connection that created them.

## Example

1.  Create two databases which both have an `IntID` table, and store a different value in each:

    <pre class="lng-console"><code><span class="gp">$</span><span class="w"> </span>sqlite3 db1.sqlite <span class="s">'CREATE TABLE IntID (id INTEGER);
                          INSERT INTO IntID (id) VALUES (100);'</span>
<span></span>
<span class="gp">$</span><span class="w"> </span>sqlite3 db2.sqlite <span class="s">'CREATE TABLE IntID (id INTEGER);
                          INSERT INTO IntID (id) VALUES (200);'</span></code></pre>

2.  Open one of the databases, attach the other, and then look up the identically-named tables:
    
    ```sqlite3
    sqlite> ATTACH DATABASE 'db2.sqlite' as db2;
    sqlite> SELECT id FROM IntID;
    100
    sqlite> SELECT id FROM main.IntID;
    100
    sqlite> SELECT id FROM db2.IntID;
    200
    ```
    
    Observe that when I query a bare `IntID`, SQLite chooses the table from the main database.
    
3.  Create a temporary table, insert a value, and query `IntID` again:

    ```sqlite3
    sqlite> CREATE TEMP TABLE IntID (id INTEGER);
    sqlite> INSERT INTO temp.IntID VALUES (300);
    sqlite> SELECT id FROM IntID;
    300
    sqlite> SELECT id FROM main.IntID;
    100
    sqlite> SELECT id FROM temp.IntID;
    300
    ```

4.  Try to read the temporary table from a different database connection, and observe that it fails:

    ```console
    $ sqlite3 db1.sqlite 'SELECT id FROM temp.IntID;'
    Error: in prepare, no such table: temp.IntID
    ```

5.  Create a table in the attached database, and observe it can be queried by the bare name, but doesn't exist in the main database:

    ```sqlite3
    sqlite> CREATE TABLE db2.NewID (id INTEGER);
    sqlite> INSERT INTO db2.NewID (id) VALUES (500);
    sqlite> SELECT id FROM NewID;
    500
    sqlite> SELECT id FROM main.NewID;
    Parse error: no such table: main.NewID
    sqlite> SELECT id FROM db2.NewID;
    500
    ```

[mjf]: https://github.com/creachadair
[bradfitz]: https://github.com/bradfitz
[sqlite-lang-naming]: https://sqlite.org/lang_naming.html
[sqlite-temp-tables]: https://sqlite.org/tempfiles.html#temp_databases
