#!/usr/bin/env python
"""
Get a JSON file recording all the stations in the UK and Ireland, and
their lat/long coordinates.

Based on data from:

*   Trainline EU (Great Britain):
    https://github.com/trainline-eu/stations

*   Wikipedia (Ireland/Northern Ireland):
    https://en.wikipedia.org/wiki/List_of_railway_stations_in_Ireland

"""

import csv
import gzip
import io
import json
import re
from urllib.request import urlretrieve

import bs4


def get_trainline_csv_rows():
    """
    Generate every row in the Trainline EU database.
    """
    filename, _ = urlretrieve(
        "https://raw.githubusercontent.com/trainline-eu/stations/master/stations.csv"
    )

    with open(filename) as infile:
        reader = csv.DictReader(infile, delimiter=";")

        for row in reader:
            yield row


def get_wikipedia_rows():
    filename, _ = urlretrieve(
        "https://en.wikipedia.org/wiki/List_of_railway_stations_in_Ireland"
    )

    with open(filename) as infile:
        soup = bs4.BeautifulSoup(infile.read(), "html.parser")

        table = soup.find("table", attrs={"class": "wikitable"})

        rows = iter(table.find_all("tr"))

        field_names = [th_tag.text.strip() for th_tag in next(rows).find_all("th")]

        for row in rows:
            yield dict(
                zip(field_names, [td_tag.text.strip() for td_tag in row.find_all("td")])
            )


if __name__ == "__main__":
    from pprint import pprint

    stations = {}

    for row in get_trainline_csv_rows():

        # The Trainline database includes stations from a lot of countries,
        # but we're only interested in stations in Great Britain.
        #
        # (The Trainline database doesn't seem to include Northern Ireland stations.)
        if row["country"] != "GB":
            continue

        # These are placeholder entries for places that have multiple stations:
        # e.g. there is no "Bristol" station, only Parkway and Temple Meads.
        #
        # If you want all trains to either station, you could ask Trainline to
        # find tickets to "Bristol", but that's not useful here.
        if row["is_city"] == "t":
            continue

        if row["id"] in {
            "22980",  # Another entry for London
            "8271",  # London Southern Railway, I have no idea
            "8243",  # Looks like an SNCF entry for Hull, maybe freight?
            "8386",  # London City Airport, isn't a Network Rail station
            "8217",  # Another SNCF entry, maybe more freight?
            "8159",  # City entry for Larne
            "8147",  # Freight entry for Fishguard Harbour
            "8038",  # Weymouth Quay, disused station that doesn't have coords
            "8035",  # Dover hoverport
            "7986",  # Dover eastern docks, freight
            "7867",  # Lincoln St. Mark's, disused station
        }:
            continue

        if row["name"] in {
            # Not actually a train station, but included in the Trainline database.
            "London Victoria Coach Station",
            # I have no idea what this is
            "Gde bretagne",
            # These are all included, but without lat/long data
            "Gatwick",
            "Gatwick Airport",
            "Gatwick\u2014Airport",
            "Devils bridge",  # Heritage railway
            # We don't need seven entries for Heathrow!
            "Heathrow Terminals 1-2-3 Bus",
            "Heathrow Terminals 1-2-3 Rail",
            "Heathrow Terminal 4 Bus",
            "Heathrow Terminal 4 Rail",
            "Heathrow Terminal 5 Bus",
            "Heathrow Terminal 5 Rail",
        }:
            continue

        coords = [row["longitude"], row["latitude"]]

        if coords == ["", ""]:
            print(f"⚠️ No coordinates for {row['name']}")
            from pprint import pprint

            pprint(row)
            continue

        stations[row["name"]] = coords

    # https://tools.wmflabs.org/geohack/geohack.php?pagename=Gatwick_Airport_railway_station&params=51.1565_N_0.1609_W_type%3Arailwaystation_region%3AGB_scale%3A10000
    stations["Gatwick Airport"] = ["-0.1609", "51.1565"]

    # https://tools.wmflabs.org/geohack/geohack.php?params=52.376051_N_3.854077_W_type%3Arailwaystation_region%3AGB&pagename=Devil%27s_Bridge_railway_station
    stations["Devil's Bridge"] = ["-3.854077", "52.376051"]

    stations["Cambridge North"] = ["0.1585111", "52.2239699"]

    for row in get_wikipedia_rows():
        if row["Location"] != "Northern Ireland":
            continue

        names = [row["Irish name"], row["English Name"]]
        names = [nm.strip() for nm in names if nm.strip()]

        # The coordinate string is in the format:
        #
        #   1°2′3″N 1°2′3″W\ufeff / \ufeff1.234°N 1.2.3.4°W\ufeff / 1.234; -1.234
        #
        # so we can split on slashes to get the decimal values.
        long_lat_coords = row["Coordinates"].split("/")[-1].strip()
        match = re.match(
            r"^(?P<longitude>-?\d+\.\d+); (?P<latitude>-?\d+\.\d+)$", long_lat_coords
        )
        assert match is not None, long_lat_coords

        stations["/".join(names)] = [match.group("latitude"), match.group("longitude")]

    # We use a semicolon to delimit station names in `managers.js` (look at how
    # we store station names in window.localStorage), so finding a station with
    # a semicolon in the name would be tricky.
    assert all(";" not in name for name in stations)

    json_string = json.dumps(stations, indent=2, sort_keys=True)
    js_string = f"const stations = {json_string};"

    with open("static/stations.js", "w") as out_file:
        out_file.write(js_string)

    min_json_string = json.dumps(stations, separators=(',',':'))
    min_js_string = f"const stations={min_json_string};"

    with open("assets/stations.min.js", "w") as out_file:
        out_file.write(min_js_string)

    print("✨ Written station coordinates to stations.js ✨")
