---
layout: article
date: 2026-08-20 10:49:28 +01:00
title: Why can’t you combine `.tar.gz` files with `cat`?
summary: To combine archives safely, I had to start by understanding the `tar` and `gzip` file formats. I learnt about tape drives, patent laws, and end-of-file markers.
topic: Computers and code
---
I'm working on a project that generates multiple `.tar.gz` archives, and I need to combine them into one final file.
I thought I could just `cat` the bytes together, but that doesn't work.
This seemingly simple task exposed my flawed understanding of `tar` and `gzip`.

To my fix my code, I first had to fix my mental model -- and that took me into tape drives, patent laws, and end-of-file markers.

## tar stands for **t**ape **ar**chive

[`tar`][wiki-tar] is a file archiver that combines multiple files and their metadata -- filenames, timestamps, directory structure -- into a single file.

It was originally designed for [magnetic tapes][wiki-magnetic-tapes], and the file structure is informed by the physical constraints of that medium:

1.  **Sequential reads.**
    Magnetic tapes are most efficient when you start at the beginning, and play forward to the end of the tape.

2.  **Append-only writes.**
    Early tapes could only append data to the end of a record, not replace existing data.

3.  **Fixed data sizes.**
    Tapes have a fixed capacity, and early tapes had fixed data block sizes.

Internally, a tar archive is a sequence of files, each broken into fixed-size blocks.
Files have a header block (with metadata like filename and file size) and data blocks (the file contents).
After the files, there are two or more blocks filled entirely with zeroes.
These form an [end-of-file (EOF) marker][wiki-eof] that tells a reader to disregard everything else in the archive.

{%
  inline_svg
  filename="tar_structure.svg"
  width="270"
  class="dark_aware"
  alt="Architecture diagram showing the internals of a tar archive. There are two files with a header and data blocks, two blocks of zeroes, and two ignored blocks."
%}

This structure mirrors physical tape: you can read files sequentially or append new ones to the end.
That sequential design is why tar remains popular for streaming over a network -- you can process incoming files immediately, without waiting to download the complete archive.

Knowing this structure helps me understand aspects of tar that I previously found confusing:

*   **File sizes must be declared upfront.**
    You need to write the file size in the header before you write any data blocks.
    When I use Python's [`TarFile.addfile` API][pydoc-tarfile-addfile], I often forget to set `tarinfo.size`, so Python writes `0` to the header and creates an empty archive.

*   **Archives can contain duplicate filenames.**
    You can't edit or delete existing blocks on tape, so you update a file by appending a new version with the same filename.
    When you unpack the archive, the later file overwrites the earlier one.

*   **Everything after the EOF marker is ignored.**
    Because physical tapes have fixed capacities, the EOF marker signals where data ends and empty tape begins.
    While tools like GNU tar have an `--ignore-zeros` flag to keep reading past EOF markers, I want to build archives that can be read with the default settings.

I tried a naïve approach of `cat`-ing tar archives, but that fails because readers stop at the first EOF marker.
Instead, I'm combining archives using Python's [tarfile module][pydoc-tarfile].
I unpack each archive, then copy its members into a new archive which will have a single EOF marker:

```python {"names":{"1":"tarfile","2":"combine_tars","3":"output_file","4":"input_files","8":"out","9":"f","14":"src","15":"member"}}
import tarfile

def combine_tars(output_file, input_files):
    """
    Combine multiple tar archives into a single archive.
    """
    with tarfile.open(output_file, "w") as out:
        for f in input_files:
            with tarfile.open(f, "r") as src:
                for member in src.getmembers():
                    out.addfile(member, src.extractfile(member))

combine_tars("numbers.tar", ["one.tar", "two.tar", "three.tar"])
```

This is more code than concatenating raw bytes, but it creates a tar archive that doesn't need special settings to read.

## gzip compresses a single stream of data

[`gzip`][wiki-gzip] is a stream compressor that takes a single file or data stream, and makes it smaller.
The compression is lossless, so you can reverse it to retrieve the original file.

Unlike tar, gzip was a response to patent laws, not physical hardware.
Reading [RFC 1952][rfc-1952] which defines the gzip file format, three design constraints reflect the time in which it was created:

1.  **Patent-free.**
    The gzip tool was written as a free software replacement for `compress`, a comprssion tool whose underlying [LZW algorithm][wiki-lzw] was protected by patents at the time.

2.  **Streamable.**
    Compressing or decompressing a gzip file must only use a small, bounded amount of memory.
    In the early 1990s, when RAM was even more scarce and expensive than it is today, the ability to process data in small, continuous chunks was essential.

3.  **Portable.**
    A gzip file should be independent of the CPU, OS, filesystem, and other aspects of the computer it was created on.
    We take this sort of portability for granted today, but it wasn't always a given.

Internally, a gzip file is a sequence of one or more "members".
Each member has a header (with metadata like original filename and modification time), the compressed data, and a trailer (with a CRC32 checksum and uncompressed size).
The file ends after the final trailer -- gzip doesn't have EOF markers.

{%
  inline_svg
  filename="gzip_structure.svg"
  width="270"
  class="dark_aware"
  alt="Architecture diagram showing the internals of a gzip file. There are two three members, each with a header, a data block, and a trailer."
%}

Conceptually, it's tempting to see members as an analogue for files, but that's not how gzip works.
Tools treat multiple members as part of the same data stream, and you can't list or extract them individually.
When you uncompress a multi-member gzip file, you only get a single stream back.

Because members come one after another and there's no EOF marker, you can concatenate gzip files by just `cat`-ing bytes:

```bash
echo "one uno eins"    | gzip > one.gz
echo "two duo zwei"    | gzip > two.gz
echo "three tres drei" | gzip > three.gz

cat one.gz two.gz three.gz > numbers.gz

gunzip --uncompress --to-stdout numbers.gz
```

## How do you combine tar.gz archives?

tar and gzip are firm friends.
tar combines a directory tree into a single stream; gzip makes that stream smaller.
Because they both support sequential reads, `.tar.gz` is very popular for streaming data over a network -- you can start processing individual files before you download the entire archive.

My mistake was trying to combine `.tar.gz` files using `cat`.
gzip plays ball, but tar throws a strop.

gzip happily combines the compressed members into a single stream, but when tar tries to read the decompressed stream, it finds the first archive's EOF marker and stops reading.
gzip would be happy to carry on, but tar has given up.

To combine `.tar.gz` files safely, I have to extract the underlying members and write them to a new file.
That means modifying my Python function above from plain read/write (`r`/`w`) to gzip-compressed read/write (`r:gz`/`w:gz`):

```python {"names":{"1":"tarfile","2":"combine_tar_gzs","3":"output_file","4":"input_files","8":"out","9":"f","14":"src","15":"member"}}
import tarfile

def combine_tar_gzs(output_file, input_files):
    """
    Combine multiple gzip compressed tar archives into a single archive.
    """
    with tarfile.open(output_file, "w:gz") as out:
        for f in input_files:
            with tarfile.open(f, "r:gz") as src:
                for member in src.getmembers():
                    out.addfile(member, src.extractfile(member))

combine_tar_gzs("numbers.tar.gz", ["one.tar.gz", "two.tar.gz", "three.tar.gz"])
```

This started as a confusing bug, but it became a fun side quest.
Now I understand how these formats work, I understand why my original code doesn't work, and I understand how I can fix it.
I can go back to my project, safe in the knowledge that I haven't missed a secret shortcut or an obvious optimisation.

[pydoc-tarfile]: https://docs.python.org/3/library/tarfile.html
[pydoc-tarfile-addfile]: https://docs.python.org/3/library/tarfile.html#tarfile.TarFile.addfile
[pydoc-tarfile-mode]: https://docs.python.org/3/library/tarfile.html#tarfile.open
[rfc-1952]: https://datatracker.ietf.org/doc/html/rfc1952
[wiki-eof]: https://en.wikipedia.org/wiki/End-of-file_marker
[wiki-gzip]: https://en.wikipedia.org/wiki/Gzip
[wiki-lzw]: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch
[wiki-magnetic-tapes]: https://en.wikipedia.org/wiki/Magnetic-tape_data_storage
[wiki-null-byte]: https://en.wikipedia.org/wiki/Null_terminator
[wiki-tar]: https://en.wikipedia.org/wiki/Tar_(computing)
