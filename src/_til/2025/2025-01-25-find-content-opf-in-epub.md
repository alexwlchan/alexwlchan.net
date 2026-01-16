---
layout: til
title: How to find the `content.opf` in an EPUB file
date: 2025-01-25 23:21:22 +00:00
tags:
  - epub
---
The `content.opf` file within an EPUB contains metadata about the book -- like the title, the author, and the subject.

To find the `content.opf` file, look for the mandatory `META-INF/container.xml` file.
This is a pointer to the `content.opf` file.
For example:

```xml
<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
   <rootfiles>
      <rootfile full-path="content.opf" media-type="application/oebps-package+xml"/>

   </rootfiles>
</container>
```
    
See also: [Anatomy of an EPUB 3 file](https://www.edrlab.org/open-standards/anatomy-of-an-epub-3-file/)
