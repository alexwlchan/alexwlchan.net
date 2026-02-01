---
layout: post
date: 2023-09-24 16:31:02 +00:00
title: Adding locations to my photos from my Apple Watch workouts
summary: My Apple Watch knows where I am, which is handy when I have a camera that doesn't.
tags:
  - python
  - photo management
colors:
  index_light: "#5b3527"
  index_dark:  "#f8e0bf"
---

A week or so ago, I was hiking around [Lake Bohinj], a gorgeous Alpine lake in northwest Slovenia.
It's a very photogenic landscape, so I was taking some pictures with my "nice" camera.
It's an Olympus that takes better photos than my iPhone, but it's quite old and it doesn't have built-in GPS -- so none of the photos have [location geotags][geotagging].

I find location data quite useful on my photos, and I was wondering if I could add it after the fact.
Although my camera doesn't know where I was, I had a walking workout running on my Apple Watch, and that was tracking my location -- could I combine the photos from my camera and the location data from my watch?

[Lake Bohinj]: https://en.wikipedia.org/wiki/Lake_Bohinj
[geotagging]: https://en.wikipedia.org/wiki/Geotagging

---

{%
  picture
  filename="confused-camera.jpg"
  width="750"
  class="full_width"
  alt="A black Olympus character looking out of a window, with a cartoon thought bubble showing a location pin and a question mark. It’s wondering what GPS and locations are."
%}

The first step was to get all the data from my walking workout.
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
  width="750"
  alt="An outline map of mostly green countryside with a blue lake (Bohinjsko jezero) in the middle. There's a thick green line that goes around the lake, showing my walking route."
%}

GPX files are XML, and the format of the Apple Health workout routes isn't especially complicated.
Here's the first few lines of a file:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx
  version="1.1"
  creator="Apple Health Export"
  xmlns="http://www.topografix.com/GPX/1/1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd"
>
  <metadata>
    <time>2023-09-19T21:04:33Z</time>
  </metadata>
  <trk>
    <name>Route 2023-09-17 2:38pm</name>
    <trkseg>
      <trkpt lon="13.887391" lat="46.277433">
        <ele>532.367857</ele>
        <time>2023-09-17T07:05:52Z</time>
        <extensions>
          <speed>1.400002</speed>
          <course>287.656214</course>
          <hAcc>2.032849</hAcc>
          <vAcc>1.793892</vAcc>
        </extensions>
      </trkpt>
      <trkpt lon="13.887373" lat="46.277437">
        <ele>532.469812</ele>
        <time>2023-09-17T07:05:53Z</time>
        <extensions>
          <speed>1.398853</speed>
          <course>283.005353</course>
          <hAcc>1.821742</hAcc>
          <vAcc>1.615372</vAcc>
        </extensions>
      </trkpt>
      …
```

The file is a series of `trkpt` ("track points"), each of which has a longitude, a latitude, an elevation and a timestamp.
The timestamps are in UTC -- the first timestamp is just after 7am, but I didn't arrive at Bohinj until just after 9am.
Like the rest of Slovenia, Bohinj is currently on UTC+2.

There are also a couple of data points which I think are something related to direction and speed?
I'm not looking into those, but it was interesting to see they're in there.
I don't think I've worked with GPS data before, and there's a bit more than I expected – I thought I'd just be getting longitude and latitude coordinates, but these extra values make sense, particular when I'm walking.

I used [lxml] to write a Python function which extracts all these track points from the file.
There are dedicated libraries for dealing with GPX files, but I already know how to use lxml and it was simple enough to write something for this one-off task.

```python
import datetime

from lxml import etree
import pytz


utc = pytz.timezone("UTC")


def get_track_points(tree: etree._ElementTree):
    """
    Generate a series of track points from an Apple Health workout route.
    """
    namespaces = {"gpx": "http://www.topografix.com/GPX/1/1"}

    for trkpt in tree.xpath("//gpx:trkpt", namespaces=namespaces):

        # e.g. 2023-09-17T07:05:52Z
        time_str = trkpt.xpath(".//gpx:time", namespaces=namespaces)[0].text
        time = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ").astimezone(utc)

        elevation = float(trkpt.xpath(".//gpx:ele", namespaces=namespaces)[0].text)

        latitude = float(trkpt.attrib["lat"])
        longitude = float(trkpt.attrib["lon"])

        yield {
            "time": time,
            "elevation": elevation,
            "latitude": latitude,
            "longitude": longitude
        }


with open("route_2023-09-17_2.38pm.gpx") as infile:
    tree = etree.parse(infile)

    for track_point in get_track_points(tree):
        print(track_point)
```

I pulled all these track points into a single Python dictionary, mapping time to location:

```python
with open("route_2023-09-17_2.38pm.gpx") as infile:
    tree = etree.parse(infile)

    locations = {
        track_point["time"]: track_point
        for track_point in get_track_points(tree)
    }
```

I discovered that there are some duplicate timestamps in the GPX file -- although there's second-level precision, occasionally it would record two locations for the same time.
The two locations were pretty close, maybe a metre or so apart.
For this sort of casual photo analysis that's fine, but it might cause issues if you need more precision.

Pulling them all into a dictionary means picking the last location that appeared in the file.
That's somewhat arbitrary, but I didn't want to spend too much time on this so I called it good.
Because they're so close together, either is fine for my purposes.

To tie this all together, I wrote a bit more Python which would find all the JPEG files from my camera, get the timestamp of that photo, and use `exiftool` to add location metadata if my workout had recorded a location at that precise timestamp:

```python
import subprocess


def get_created_time(jpeg_path, *, camera_timezone):
    """
    Returns the created time of a photo, according to ``exiftool``.
    """
    created_time_str = subprocess.check_output([
        "exiftool", "-s3", "-DateTimeOriginal", jpeg_path
    ]).decode("ascii").strip()

    # e.g. 2023:09:17 10:40:49
    created_time = datetime.datetime.strptime(created_time_str, "%Y:%m:%d %H:%M:%S")

    # Assume the camera was set to match the timezone where the photo
    # was taken; convert the timestamp to UTC first.
    return timezone.localize(created_time).astimezone(utc)


def set_location(jpeg_path, *, location_info):
    """
    Set the location information on a file using ``exiftool``.
    """
    # The Apple Watch locations record latitude/longitude/elevation
    # as a single value, whereas exiftool wants an absolute value
    # and a direction.
    #
    # e.g. the Apple Watch might record a position as (37.3346, -122.0090),
    # which exiftool wants to see as (37.3346, N, 122.0090, W).
    subprocess.check_call([
        "exiftool",
        f"-GPSLatitude={abs(location_info['latitude'])}",
        f"-GPSLatitudeRef={"N" if location_info['latitude'] > 0 else 'S'}",
        f"-GPSLongitude={abs(location_info['longitude'])}",
        f"-GPSLongitudeRef={"E" if location_info['longitude'] > 0 else 'W'}",
        f"-GPSAltitude={abs(location_info['elevation'])}",
        f"-GPSAltitudeRef={"0" if location_info['elevation'] > 0 else '1'}",
        jpeg_path
    ])


# See https://alexwlchan.net/2023/snake-walker/ for get_file_paths_under()
for jpeg_path in get_file_paths_under("100_OLYMP", suffix=".jpg"):

    slovenia = pytz.timezone("Europe/Ljubljana")
    created_time = get_created_time(jpeg_path, camera_timezone=slovenia)

    try:
        location_info = locations[created_time]
    except KeyError:
        pass
    else:
      set_location(jpeg_path, location_info=location_info)
```

This code has a big assumption at its core: that my Watch will have recorded a location at the precise second I took each photo.
In practice, that seems to work well enough -- I don't know if my Watch is doing second-by-second location, but I'd stand still to take my photos, and it would record at least one data point in that time.
All my photos from Bohinj got tagged.

If this was an issue, you could write a looser heuristic to matching photos to location data in the workout -- for example, using any location that was recorded within a few seconds of the photo being taken.
But "same second" worked fine for me, so that's all I've done.

After I ran this code, I did some spot-checking of individual photos -- it took a few tries to get the timezone handling correct.
I'd taken a photo of the *"Welcome to Bohinj"* sign right after I got off the bus, and that turned out to be super helpful -- I knew exactly where it was, and I could keep tweaking my code until that photo got the right location.

I was once given a tip: when travelling between time zones, take a photo of a clock that's correctly set to the local time.
That way, you can easily correct the time offset later if your camera was configured incorrectly.
If I plan to reuse this location tagging code, I'd use the same trick, but with a photo of something in a known location.

---

Once this was done, I imported all the files into my Photos Library, and voila: I could see all my photos plotted on a map, even though I'd taken them on a camera without GPS support.

{%
  picture
  filename="photos_on_map.png"
  width="950"
  class="screenshot"
  alt="A map view of Lake Bohinj. Dotted around the map are small markers with a photo and number, showing the number of photos taken at that exact location."
%}

I'm pretty happy with this project -- for half an hour's work, I have a nicely-tagged set of photos and a better understanding of the location data recorded by my Apple Watch.

[support]: https://support.apple.com/en-gb/guide/iphone/iph5ede58c3d/ios#iphe962dcbd2
[gpx]: https://en.wikipedia.org/wiki/GPS_Exchange_Format
[lxml]: https://lxml.de/index.html
