---
layout: post
title: Adding locations to my photos from my Apple Watch workouts
summary: My Apple Watch knows where I am, which is handy when I have a camera that doesn't.
tags: python photo-management
colors:
  index_light: "#5b3527"
  index_dark:  "#f8e0bf"
---

A week or so ago, I was hiking around [Lake Bohinj], a gorgeous Alpine lake in northwest Slovenia.
It's a very photogenic landscape, so I was taking some pictures with my "nice" camera.
It's an Olympus that takes better photos than my iPhone, but it doesn't have built-in GPS -- so none of the photos have [location geotags][geotagging].

I find location data quite useful on my photos, and I was wondering if I could add it after the fact.
Although my camera doesn't know where I was, I had a hiking workout running on my Apple Watch, and that was tracking my location -- could I combine the photos from my camera and the location data from my watch?

[Lake Bohinj]: https://en.wikipedia.org/wiki/Lake_Bohinj
[geotagging]: https://en.wikipedia.org/wiki/Geotagging

{%
  picture
  filename="confused-camera.jpg"
  width="750px"
  class="full_width"
%}

The first step was to get all the data from my hiking workout.
I was able to export the data from the Health app on my iPhone, following the [instructions in an Apple Support document][support]:

> You can export all of your health and fitness data from Health in XML format, which is a common format for sharing data between apps.
>
> 1.  Tap your picture or initials at the top right.
>
>     If you don’t see your picture or initials, tap Summary or Browse at the bottom of the screen, then scroll to the top of the screen.
>
> 2.  Tap Export All Health Data, then choose a method for sharing your data.

When I tried this, my iPhone said it would take "a few moments".
It took much longer than that, and the lack of progress bar made me wonder if it was broken.

But it did eventually finish, and fifteen minutes later, I had a 174MB ZIP file full of my health data.
When I unzipped it, this is what it looked like inside:

    apple_health_export/
      ├─ export.xml
      ├─ export_cda.xml
      ├─ electrocardiograms/
      │    ├─ ecg_2020-12-27.csv
      │    └─ ...10 other files
      └─ workout-routes/
           ├─ route_2020-12-26_1.47pm.gpx
           ├─ route_2020-12-27_1.04pm.gpx
           └─ ...1556 other files

The GPX files are the interesting thing here -- GPX is [a standard format][gpx] for passing around GPS data.
If I preview one of those files in Quick Look, I can see my walking route shown as a thick green line on a map:

{%
  picture
  filename="bohinj_gpx.png"
  width="750px"
%}



[gpx]: https://en.wikipedia.org/wiki/GPS_Exchange_Format

---

This was a lie.
I don't know if I have an unusually large amount of Health data, but it took closer to 15 minutes to export everything.

I got a 174MB ZIP file, which

[support]: https://support.apple.com/en-gb/guide/iphone/iph5ede58c3d/ios#iphe962dcbd2


## step 1: get all location data

Export all health data from my iPhone

Took a while – maybe 10–15 mins? 173MB ZIP archive

inside is a folder called `workout-routes` with a stack of GPX files

what is GPX?

## step 2: get a list of locations from GPX

can get list of locations from GPX
could use library e.g. pygpx, but XML simple enough for me to follow

could find other uses for this, e.g. ned batchelder

## step 3: match locations to photos

use exiftool!

## done

didn't manage to tag all my photos, e.g. when I'd paused on the hike and it wasn't tracking
I could keep going, e.g. extrapolate location
but not worth it

good enough for half an hour's work

---

Export all health data from my iPhone

Took a while – maybe 10–15 mins? 173MB ZIP archive

inside is a folder called `workout-routes` with a stack of GPX files

something like this:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx
  version="1.1"
  creator="Apple Health Export"
  xmlns="http://www.topografix.com/GPX/1/1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <metadata>
    <time>2023-09-19T21:04:35Z</time>
  </metadata>
  <trk>
    <name>Route 2023-09-18 8:12am</name>
    <trkseg>
      <trkpt lon="14.505981" lat="46.050438">
        <ele>298.819464</ele>
        <time>2023-09-18T06:58:37Z</time>
        <extensions>...</extensions>
      </trkpt>
      <trkpt lon="14.505974" lat="46.050424">
        <ele>298.909533</ele>
        <time>2023-09-18T06:58:38Z</time>
        <extensions>...</extensions>
      </trkpt>
      <trkpt lon="14.505968" lat="46.050411">
        <ele>298.990401</ele>
        <time>2023-09-18T06:58:39Z</time>
        <extensions>...</extensions>
      </trkpt>
```

not so good in downstairs/underground caves!!!

```python
#!/usr/bin/env python3

import collections
import datetime
import json
import os
import zipfile

from lxml import etree


locations = {}

namespaces = {"gpx": "http://www.topografix.com/GPX/1/1"}

with zipfile.ZipFile("export.zip") as zf:
    for name in zf.namelist():
        if not name.startswith("apple_health_export/workout-routes/"):
            continue

        if not name.startswith("apple_health_export/workout-routes/route_2023-09"):
            continue

        contents = zf.read(name)

        gpx_data = etree.fromstring(contents)

        track_points = gpx_data.xpath("//gpx:trkpt", namespaces=namespaces)

        for tp in track_points:
            # e.g. 2023-09-12T08:03:54Z
            time = datetime.datetime.strptime(
                tp.xpath(".//gpx:time", namespaces=namespaces)[0].text,
                "%Y-%m-%dT%H:%M:%SZ",
            )

            elevation = tp.xpath(".//gpx:ele", namespaces=namespaces)[0].text

            # what about duplicates?

            # e.g.              '2023-09-12T08:09:23Z': [('51.525534', '-0.134476'),
            #                          ('51.525534', '-0.134477')],

            locations[time] = {
                "latitude": float(tp.attrib["lat"]),
                "longitude": float(tp.attrib["lon"]),
                "elevation": float(elevation),
            }

import os


def get_file_paths_under(root=".", *, suffix=""):
    """
    Generates the absolute paths to every matching file under ``root``.
    """
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in sorted(filenames):
            p = os.path.join(dirpath, f)

            if os.path.isfile(p) and f.lower().endswith(suffix):
                yield p


import subprocess
import tqdm

i = 0

for photo in tqdm.tqdm(get_file_paths_under("100OLYMP/New Folder With Items/", suffix=".jpg")):
    created_time = datetime.datetime.strptime(
        subprocess.check_output(["exiftool", "-s3", "-DateTimeOriginal", photo]).decode("ascii").strip(),
        "%Y:%m:%d %H:%M:%S",
    )

    try:
        locations[created_time]
    except KeyError:
        continue


    # print(created_time)

    info = locations[created_time]

    # print(photo, info)

    subprocess.check_call([
        'exiftool',
        f'-GPSLatitude={abs(info["latitude"])}',
        f'-GPSLatitudeRef={"N" if info["latitude"] > 0 else "S"}',
        f'-GPSLongitude={abs(info["longitude"])}',
        f'-GPSLongitudeRef={"E" if info["longitude"] > 0 else "W"}',
        f'-GPSAltitude={abs(info["elevation"])}',
        f'-GPSAltitudeRef={"0" if info["elevation"] > 0 else "1"}',
        photo
    ])

    i += 1

print(i)
```