---
layout: til
title: "Using TransportAPI and geopy to get the distance between stations"
date: 2019-05-03T08:40:51Z
tags:
  - trains
  - python
---
Here's a quick snippet I wrote to play with [TransportAPI](https://developer.transportapi.com) and the [geopy library](https://pypi.org/project/geopy/).

One thing that quickly becomes clear running this code is that searching for stations with free text is hard; if I ever want to use TransportAPI properly, I should switch to some sort of filter or ID-based lookup instead.

TransportAPI has a free tier that allows you to make 30 requests a day without paying, which is why I tried it for this experiment.

```python
import typing

import geopy.distance  # pip install geopy==2.4.1
import httpx  # pip install httpx==0.28.1


APP_ID = "[redacted]"
APP_KEY = "[redacted]"


client = httpx.Client(params={"app_id": APP_ID, "app_key": APP_KEY})


def lookup_station(station_name: str) -> typing.Any:
    """
    Look up a railway station in TransportAPI.
    """
    resp = client.get(
        "https://transportapi.com/v3/uk/places.json",
        params={"query": station_name, "type": "train_station"},
    )
    resp.raise_for_status()

    members = resp.json()["member"]

    if len(members) == 0:
        raise ValueError(f"Could not find any matching stations for {station_name!r}")
    elif len(members) > 1:
        raise ValueError(
            f"Fould multiple matching stations for {station_name!r}: {members}"
        )

    return members[0]


def distance_between(station1, station2):
    pos1 = (station1["longitude"], station1["latitude"])
    pos2 = (station2["longitude"], station2["latitude"])
    return geopy.distance.geodesic(pos1, pos2)


if __name__ == "__main__":
    leighton_buzzard = lookup_station("LTNBZRD")
    brighton_and_hove = lookup_station("BRGHLRD")
    print(repr(distance_between(leighton_buzzard, brighton_and_hove)))
```

(I'm saving this TIL in 2025 after I found a screenshot in an old folder.
I can't remember what this project was now, but I thought the code and use of TransportAPI worth saving.)
