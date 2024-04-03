---
layout: post
title: Playing with snapshots of Wikimedia Commons structured data
summary: A few things I learnt while poking around in the large snapshots of Wikimedia data.
tags: 
  - python
  - data-science
colors:
  index_light: "#945e20"
  index_dark:  "#eeb364"
---

Recently I've been playing with [structured data on Wikimedia Commons][sdc].
This is human and machine-readable metadata attached to files on Commons, [for example][example]:

{%
  picture
  filename="wmc_structured_data.png"
  width="646px"
  class="screenshot"
%}

These two bits of metadata tell us what's in the photo, and who took it.
We can query this metadata across Commons to, say, find [other pictures][query] of yellow papillae flatworms.
There are [thousands of possible properties][property_list] that can be added to a file.

As part of my work, I wanted to look through how a couple of properties were used – among other things, how Flickr URLs are saved in the [source of file][P7482] property.
Wikimedia publish [weekly snapshots][snapshots] of the structured data, and I thought that would be a good way to find what I needed.
I'd go through the entire snapshot and pull out the properties I was interested in.

These snapshots are the biggest data set I've worked with to date, and I thought it would be worth noting a couple of useful things I spotted along the way.

[property_list]: https://www.wikidata.org/wiki/Wikidata:Database_reports/List_of_properties/all
[query]: https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=haswbstatement%3AP180%3DQ7799832
[sdc]: https://commons.wikimedia.org/wiki/Commons:Structured_data
[example]: https://commons.wikimedia.org/wiki/File:Yellow_papillae_flatworm_(Thysanozoon_nigropapillosum).jpg
[snapshots]: https://dumps.wikimedia.org/other/wikibase/commonswiki/
[P7482]: https://www.wikidata.org/wiki/Property:P7482

## Resumable downloads with curl

The first challenge was saving a snapshot locally -- they're pretty big!
I was trying to get `commons-20231009-mediainfo.json.bz2`, which is ~29GB, and my browser was struggling to download it reliably.
The download would take multiple hours, and it kept flaking out.

(There seems to be a limit on how fast Wikimedia will serve the file – even on a fast Internet connection, I couldn't get past ~3MB/s.
This makes sense as a way to avoid overwhelming their servers, and also means it'll take multiple hours to download.)

I was considering writing my own download manager to do chunked or resumable downloads, but luckily I checked what curl does first.
It has a [`--continue-at` flag][c_flag], which is exactly what I wanted -- if a download gets interrupted, it resumes a download from where you left off.

This allowed me to run a simple command:

```
curl \
  --location \
  --remote-name \
  --continue-at - \
  https://dumps.wikimedia.org/other/wikibase/commonswiki/20231009/commons-20231009-mediainfo.json.bz2    
```

I had to run this a couple of times before it downloaded the entire snapshot, but eventually I had a complete blob of compressed JSON sitting on my disk.
Sweet!

[c_flag]: https://curl.se/docs/manpage.html#-C

---


The snapshots are big – the one I downloaded is `commons-20231009-mediainfo.json.bz2`, which is about 29GB.


It takes several hours to download, and a faster Internet connection won't help – Wikimedia limits how fast you can download the file, presumably to avoid overwhelming their servers.

---

wikimedia commons structured data
big data, biggest data set I've worked with by some margin

  commons-20231009-mediainfo.json.bz2
  29.22 GB compressed, expands to 356.7 GB uncompressed
  91837635 records



wmc_structured_data.png


```consol
$ bzcat /Users/alexwlchan/repos/flickypedia/duplicates_from_sdc/commons-20231009-mediainfo.json.bz2 | awk '{print length}' > line_lengths2.txt
```


1. resumable downloads with curl

  first challenge is downloading it -- snapshot download takes several hours
  (and a faster internet connection won't help -- rate limits on WMC size, to avoid overwhelming their servers)

  turns out curl supports `--resumable`

  sweet!

2. a generator to pass the SDC snapshots

fairly simple json generator

```python
def get_structured_data_records(path):
    """
    Given a snapshot of SDC from Wikimedia Commons, generate every entry.
    """
    # The file is returned as a massive JSON object, but we can
    # stream it fairly easily: there's an opening [, then one
    # object per line, i.e.:
    #
    #     [
    #       {…},
    #       {…},
    #       {…}
    #     ]
    #
    # So if we go line-by-line, we can stream the file without having
    # to load it all into memory.
    
    # based on https://www.wikidata.org/wiki/Wikidata:Database_download#JSON_dumps_(recommended)
    with bz2.open(path) as in_file:
        for line in in_file:
            if line.strip() in {b"[", b"]"}:
                continue

            yield json.loads(line.replace(b",\n", b""))
```

    comment is link to original docs page
    but follows SO policy: include key info in comment, so in the link changes it's still useful
    
    * what if original link dies?
    * what if original link changes?

3. using exclusive file open to avoid erasing my progress

```python
with open('output.csv', 'x') as out_file:
    writer = csv.DictWriter(out_file, …)
    
    for sdc_record in get_structured_data_records(path):
        # …
        # do some processing
        # …
        writer.writerow(processed_record)
```

but takes a long time to produce!
multiple hours

so open CSV in exclusive-creation mode
I don't want to re-run it and inadvertently erase hours of progress (say, because my shell autosuggested the command)

if I try to re-run my script with exclusive mode
am blocked!

FileNotFoundError

useful one to bear in mind for data processing scripts
