---
layout: post
date: 2021-10-19 19:11:45 +0000
title: Programatically finding the original filename of a photo in the macOS Photos Library
summary: If you're looking at a UUID'd file in the PhotosLibrary package, how do you find its original filename?
tags:
  - macos
colors:
  index_light: "#1582c6"
  index_dark:  "#8fcff4"
---

I was doing some poking around in the Photos Library recently, and found something that might be useful to other people.

If you enable ["Download Originals to this Mac"](https://support.apple.com/en-gb/guide/photos/phtf5e48489c/6.0/mac/11.0#phtbfc950237), and you look inside the Photos Library package, you'll find all your full-resolution original photos:

{%
  picture
  filename="photos_structure.png"
  alt="A Finder window showing the path 'Photos Library.photoslibrary > originals > 6 > 682DB554-618E-42D6-92A1-3695CFF10D3B.orf'."
  width="748"
%}

Problem is, these files are named with UUIDs, rather than the original filenames set by the camera (e.g. `IMG_1770.jpg` or `PA090075.ORF`).
For what I was doing, I wanted that original filename.

The Photos Library does record this information, which you can get inside the app by selecting "Window > Info (⌘I)" – but what if you're starting from the folder full of files?
How do I find the camera filename from a UUID'd file?

The information lives in the Photos database, which is a SQLite database:

```console
$ sqlite3 "file:///Users/alexwlchan/Pictures/Photos Library.photoslibrary/database/Photos.sqlite?mode=ro"
```

Then a SQL query like this will retrieve the original filename:

```sql
SELECT ZORIGINALFILENAME FROM ZCLOUDMASTER
INNER JOIN ZGENERICASSET ON ZCLOUDMASTER.Z_PK = ZGENERICASSET.ZMASTER
WHERE ZGENERICASSET.ZFILENAME = "682DB554-618E-42D6-92A1-3695CFF10D3B.orf";
```

I found this by getting a list of all SQL tables in the database, then looking at the column names for interesting-sounding fields.
Other people have done more sophisticated analysis of the Photos database, but for what I was doing this was plenty.

{% update "2022-11-25" %}
While working on a different project, I discovered another way to do this using AppleScript.
The scripting dictionary for Photos.app allows you to address media items by UUID, so you can do something like:

{% code lang="applescript" wrap="true" %}
tell application "Photos" to get filename of media item {id: "682DB554-618E-42D6-92A1-3695CFF10D3B"}
{% endcode %}

This is quite a bit slower than accessing the SQLite database directly, but it's less likely to break in future versions of Photos.
Depending on what you're doing, this might be more convenient.
{% endupdate %}