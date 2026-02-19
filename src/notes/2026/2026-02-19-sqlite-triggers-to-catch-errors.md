---
layout: note
title: Use SQL triggers to prevent overwriting a value
summary: A trigger lets you run an action when you `INSERT`, `UPDATE` or `DELETE` a value.
date: 2026-02-19 19:50:44 +00:00
topic: SQLite
---
Today I wanted to write a value to a SQLite database, and error if the database already had a conflicting value.

There are a variety of ways you could do this -- I decided to read the current stored value and check it in Go -- but I also discovered there's a way you could do it in SQL alone using [`CREATE TRIGGER`][sql-create-trigger].
I did this with SQLite, but it looks like this is supported by other SQL dialects, including PostgreSQL and MySQL.

## Setup

Let's create a table which we'll use to store write-once values:

```sqlite3
sqlite> CREATE TABLE KeyValuePairs (
   ...>     Key   TEXT NOT NULL PRIMARY KEY,
   ...>     Value TEXT NOT NULL
   ...> );
```

If I try to `INSERT` a duplicate key into this table, it fails:

```sqlite3
sqlite> INSERT INTO KeyValuePairs (Key, Value)
   ...> VALUES ('Colour', 'Red');
sqlite> INSERT INTO KeyValuePairs (Key, Value)
   ...> VALUES ('Colour', 'Green');
Runtime error: UNIQUE constraint failed: WriteOnce.Key (19)
```

But I can overwrite an existing key with an `INSERT OR REPLACE` or `UPDATE`:

```sqlite3
sqlite> INSERT OR REPLACE INTO KeyValuePairs (Key, Value)
   ...> VALUES ('Colour', 'Green');
sqlite> SELECT * FROM WriteOnce;
Parse error: no such table: WriteOnce
sqlite> SELECT * FROM KeyValuePairs;
Colour|Green

sqlite> UPDATE KeyValuePairs
   ...> SET Value = 'Blue'
   ...> WHERE Key = 'Colour';
sqlite> SELECT * FROM KeyValuePairs;
Colour|Blue
```

## Adding triggers

Let's suppose I want to prevent somebody from overwriting the `Colour` key with a different value.

I can use [`CREATE TRIGGER`][sql-create-trigger] to create a trigger on my table -- that is, an action that runs whenever I perform an `INSERT`, `UPDATE` or `DELETE`.

For the `INSERT` case, I look for an existing key-value pair, and check if the existing value matches the inserted value.
If not, I call a special [`RAISE()` function][sqlite-raise] which aborts the transaction, and nothing is written:

```sqlite3
sqlite> CREATE TRIGGER IF NOT EXISTS prevent_insert_overwrite_colour
   ...> BEFORE INSERT ON KeyValuePairs
   ...> FOR EACH ROW
   ...> WHEN NEW.Key = 'Colour'
   ...> AND EXISTS (SELECT 1 FROM KeyValuePairs WHERE Key = 'Colour')
   ...> BEGIN
   ...>     SELECT CASE
   ...>         WHEN (
   ...>             SELECT Value
   ...>             FROM KeyValuePairs
   ...>             WHERE Key = 'Colour'
   ...>         ) != New.Value
   ...>         THEN RAISE(ABORT, 'Error: Colour already exists with a different value.')
   ...>     END;
   ...> END;
```

For the `UPDATE` case, I can use the `OLD` reference to inspect the existing value in the table:

```sqlite3
sqlite> CREATE TRIGGER IF NOT EXISTS prevent_update_overwrite_colour
   ...> BEFORE UPDATE ON KeyValuePairs
   ...> FOR EACH ROW
   ...> WHEN NEW.Key = 'Colour'
   ...> AND EXISTS (SELECT 1 FROM KeyValuePairs WHERE Key = 'Colour')
   ...> BEGIN
   ...>     SELECT CASE
   ...>         WHEN OLD.Value != New.Value
   ...>         THEN RAISE(ABORT, 'Error: Colour already exists with a different value.')
   ...>     END;
   ...> END;
```

With these two triggers in place, running an `INSERT` or `UPDATE` that matches the existing value is a no-op:

```sqlite3
sqlite> INSERT OR REPLACE INTO KeyValuePairs (Key, Value)
   ...> VALUES ('Colour', 'Blue');
sqlite> UPDATE KeyValuePairs
   ...> SET Value = 'Blue'
   ...> WHERE Key = 'Colour';
sqlite> SELECT * FROM KeyValuePairs;
```

But trying to `INSERT` or `UPDATE` a conflicting value throws my custom error, and leaves the value as-is:

```sqlite3
sqlite> INSERT OR REPLACE INTO KeyValuePairs (Key, Value)
   ...> VALUES ('Colour', 'Orange');
Runtime error: Error: Colour already exists with a different value. (19)
sqlite> UPDATE KeyValuePairs
   ...> SET Value = 'Purple'
   ...> WHERE Key = 'Colour';
Runtime error: Error: Colour already exists with a different value. (19)
sqlite> SELECT * FROM KeyValuePairs;
Colour|Blue
```

The projects I work on usually put this sort of logic in the application code, but it's neat to see how this could be implemented in the database layer.

[sql-create-trigger]: https://sqlite.org/lang_createtrigger.html
[sqlite-raise]: https://sqlite.org/lang_createtrigger.html#the_raise_function
