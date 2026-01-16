---
layout: til
title: How to do offline geo-lookups of IP addresses
summary: |
  MaxMind offer databases you can do to look up IP addresses without sending the address off to a remote service.
date: 2024-01-19 10:25:34 +00:00
tags:
  - python
  - networking
---
I was experimenting with web analytics, and I wanted a way to look up the country for an IP address -- in a privacy-preserving way.

There are lots of web APIs for doing IP address lookup, e.g.

```console
$ curl "https://api.ipregistry.co/1.2.3.4?key=tryout"
```

These are suitable for certain one-off tasks, but you're sending the IP address off to a third-party service.
If I use this in an analytics package, I'm handing a complete list of visitor addresses to this service.
Ick!

(Plus making an HTTP request for each IP address probably introduces lots of latency.)

A [Stack Overflow answer][so] pointed me at [MaxMind].
I was able to download a free country database from their site, which is about 6.4MB in "MaxMind DB" format -- a [database format][mmdb] designed for fast IP address lookups.

I can then use [the maxminddb Python library][maxminddb] to open the database and look up IP addresses:

```python
import maxminddb

with maxminddb.open_database('GeoLite2-Country_20240116/GeoLite2-Country.mmdb') as reader:
    print(reader.get('52.85.118.55'))
    # {'continent': {'code': 'NA', 'geoname_id': 6255149, …
```

Note that this method can sometimes return `None`, if the IP address isn't in the database -- or in this case, if it's an IP address reserved for testing purposes.

```python
with maxminddb.open_database('GeoLite2-Country_20240116/GeoLite2-Country.mmdb') as reader:
    print(reader.get('192.0.2.0'))
    # None
```

[so]: https://stackoverflow.com/q/17182203/1558022
[MaxMind]: https://www.maxmind.com/en/home
[mmdb]: https://maxmind.github.io/MaxMind-DB/
[maxminddb]: https://pypi.org/project/maxminddb/
