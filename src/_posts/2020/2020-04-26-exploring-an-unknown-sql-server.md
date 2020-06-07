---
layout: post
date: 2020-04-26 17:53:53 +0000
title: Exploring an unknown SQL server
summary: You're handed a SQL server which has some data, but you don't know anything about the schema. What do you do?
category: Programming and code
tags: programming mysql
---

I've been helping to decommission an old application at work recently, and part of that process was verifying we'd got all the important data out.
All the data was stored in a Microsoft SQL Server database, hosted by our IT department.
Getting it out should be simple enough, right?

Problem is, we knew almost nothing about the database.
The application was written by a third-party vendor, who we were no longer paying for support.
Aside from a few existing queries that answered very specific questions, we didn't know how to get data out of the database.

All we had was a read-only endpoint into the database server.
Thus, we faced a question:

**How do you find your way around a SQL database you know nothing about?**

I did a bunch of digging, and I did eventually find the data we needed.
The project is done now, and we'll turn the database off soon.
I won't share details of this specific database, but here's the general pattern of how I teased out the useful data:

1.  **Find out what tables are in the database.**

    ```sql
    SELECT * FROM sys.tables
    ```

    This gave me a list of all the tables in the database -- 138 of them.
    They all had fairly sensible names, and I could guess the purpose of at least some of the tables.
    That let me pick a few tables to dig into further.

2.  **Look at the schema of tables that sound interesting.**

    ```sql
    SELECT * FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_NAME = 'Shapes'
    ```

    This gave me a list of columns in each table -- what sort of data does this table contain?
    This helped me work out whether a table contained data that would be useful.

    A good thread to tug on was to look at any columns with foreign keys -- that is, columns that pointed to rows in another table of the database.
    For example, if the `Shapes` table contained a column `ColourID`, that's a good hint I should look through the `Colours` table.

    That helped me get an idea of how the tables were connected, and to find tables with interesting data that I'd initially overlooked.
    Eventually I was able to sketch out how the data I wanted was spread across different tables:

    <img src="/images/2020/database_tables.svg" alt="A collection of green and yellow boxes joined by arrows">

3.  **Look at the data within the tables.**

    ```sql
    SELECT * FROM Shapes
    ```

    Once I knew which tables were interesting, I pulled out all the rows and dumped them as CSV files on my local disk.
    That let me work with data in tools I'm much more comfortable with, and start to combine data from across multiple tables.

    I'm sure you could do the same thing with an appropriate JOIN statement, but I'm more comfortable with things like Python and Jupyter Notebook.

Once I'd worked it out, this pattern worked pretty well for extracting the data we needed: guess at some relevant tables, use foreign keys to find connections into other tables, then dump all the data and start sifting through it.

I don't know if or when I'll do a task like this again, but doing it once and finding a general pattern should make it faster next time round.
The SQL syntax may vary, but the steps won't.
