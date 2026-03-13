---
layout: note
date: 2026-03-13 23:29:39 +00:00
title: The file(1) command can read SQLite databases
summary: It can identify a SQLite database and give you basic information about the version, page count, encoding, and more.
topic: SQLite
---

Here's a neat trick that [Percy][percy] showed me today: the [file(1) command][file1] is able to recognise SQLite databases, and print some information about the structure of the database.

Here's an example from my Mac:

```console {"wrap":true}
$ file example.db
example.db: SQLite 3.x database, last written using SQLite version 3050004, file counter 89, database pages 4, cookie 0x2, schema 4, UTF-8, version-valid-for 89
```

These values are read from the [database header][sqlite-database-header], the first 100 bytes of the file which include information about the database.
A couple of fields stood out to me:

*   **The SQLite version.**
    This is an integer, specifically [`SQLITE_VERSION_NUMBER`][sqlite-version-number], which is a representation of the version number.
    In this example, `3050004` means the database was last written by SQLite 3.50.4.

*   **The [file (change) counter][sqlite-file-counter] counts changes to the database.**
    If multiple processes are working in the same database, they can detect when another process made a change, and invalidate their page cache.
    
    I was surprised that this value was so low for our production databases at work (just 1196), but the SQLite docs explain that if you run your database in WAL mode -- which we do -- changes are tracked through the wal-index, and so the change counter might not be incremented.
    That must be happening in our databases.

*   **The [(schema) cookie][sqlite-schema-cookie] gets incremented whenever the database schema changes.**
    I ran a quick example and I can see it increasing from `0x2` to `0x3` in my example database:

    ```console {"wrap":true}
    $ file example.db
    example.db: SQLite 3.x database, last written using SQLite version 3050004, file counter 90, database pages 4, cookie 0x2, schema 4, UTF-8, version-valid-for 90

    $ sqlite3 example.db 'CREATE TABLE NewTable(x);'

    $ file example.db
    example.db: SQLite 3.x database, last written using SQLite version 3050004, file counter 91, database pages 5, cookie 0x3, schema 4, UTF-8, version-valid-for 91
    ```
    
    The field that file(1) labels as "schema" is the [schema format number][sqlite-schema-format-number], and tracks the version of SQL formatting used in the database.
    As of 13 March 2026, schema format 4 is the highest possible value, and it has been since January 2006.

*   **The [user version field][sqlite-user-version] is an integer for "applications to use however they want" which SQLite doesn't read.**
    I imagine this might be quite useful for storing, say, a schema version in an easily accessible location.
    
    You can set it using the `user_version` pragma, and then it appears in the file(1) output:
    
    ```console {"wrap":true}
    $ sqlite3 example.db 'PRAGMA user_version = 42;'

    $ file example.db
    example.db: SQLite 3.x database, user version 42, last written using SQLite version 3050001, file counter 92, database pages 5, cookie 0x3, schema 4, UTF-8, version-valid-for 92
    ```

*   **The [application ID][sqlite-application-id] is a field to identify the application that "owns" the database.**
    Lots of applications use SQLite as their storage format, and they can record their ID in this field.

    There are well-known values in [`magic.txt`][magic-txt] in the SQLite repository.
    If you use one of these, file(1) adds the human-readable name to its output:

    ```console {"wrap":true}
    $ sqlite3 example.db 'PRAGMA application_id = 0x0f055112;'

    $ file example.db
    example.db: SQLite 3.x database (Fossil checkout), last written using SQLite version 3050001, file counter 94, database pages 5, cookie 0x3, schema 4, UTF-8, version-valid-for 94
    ```
    
    If you use a different value, file(1) prints the literal value:
    
    ```console {"wrap":true}
    $ sqlite3 example.db 'PRAGMA application_id = 0x42424242;'

    $ file example.db
    example.db: SQLite 3.x database, application id 1111638594, last written using SQLite version 3050001, file counter 95, database pages 5, cookie 0x3, schema 4, UTF-8, version-valid-for 95
    ```
    
    This lookup comes from a `sql` "magic" file [which ships with file(1)][file1-magic], embedding all the values from SQLite's `magic.txt` and many more besides.

[file1]: https://alexwlchan.net/man/man1/file.html
[file1-magic]: https://github.com/file/file/blob/fac0603d48af08d53547b795385abef4337d6d5f/magic/Magdir/sql#L207-L214
[magic-txt]: https://sqlite.org/src/artifact?ci=trunk&filename=magic.txt
[percy]: https://github.com/oxtoacart
[sqlite-application-id]: https://sqlite.org/fileformat.html#application_id
[sqlite-database-header]: https://sqlite.org/fileformat.html#the_database_header
[sqlite-file-counter]: https://sqlite.org/fileformat.html#file_change_counter
[sqlite-schema-cookie]: https://sqlite.org/fileformat.html#schema_cookie
[sqlite-schema-format-number]: https://sqlite.org/fileformat.html#schema_format_number
[sqlite-user-version]: https://sqlite.org/pragma.html#pragma_user_version
[sqlite-version-number]: https://sqlite.org/c3ref/c_scm_branch.html
