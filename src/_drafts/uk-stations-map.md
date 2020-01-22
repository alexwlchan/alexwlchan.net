---
layout: post
title: An interactive map of British railway stations 🚂
summary:
category: Glitch apps
link: https://uk-stations-map.glitch.me/
---

Here's another fun project I've been working on: a map that you can use to plot which railway stations you've visited.

I was a visiting a new-to-me station recently ([Letchworth Garden City]), and I started wondering what other stations I'd visited.
On the return journey, I wrote down a list, but a flat list isn't very interesting.
What if I plotted the stations on a map?

When I got home, I started mucking around to see what I could do.
I discovered the [Leaflet.js] library for creating maps, which I combined with tiles from [OpenStreetMap] to create a backdrop for the UK.
Leaflet gives you all the stuff we've come to expect from digital maps: panning, pinch to zoom, loading detail to match the zoom level, and so on.
I've never done anything with maps before, and this was very pleasant.

Leaflet also allows you add markers to a map, like so:

```javascript
L.circleMarker([lat, long], {
  fill: true,
  color: "#0b9e00",
  fillColor: "rgba(11, 158, 0, 0.3)",
  radius: 5,
}).addTo(map);
```

So if I could look up longitude/latitude data for railway stations, I could throw that into Leaflet and I'd have my map.

The Network Rail APIs are pretty inscrutable, but I'd used [TransportAPI] in the past, and that was pretty good for looking up stations one-by-one.
I got the coordinates for the 30-odd stations I remembered visiting, and created my map.
I posted [a screenshot on Twitter](https://twitter.com/alexwlchan/status/1216020489019297793), which people seemed to enjoy.

I'd hoped to turn it into an interactive web app, so other people could use it too, but building the station picker seemed hard.
There are over 2000 stations in the UK.
How do you select the ones you've visited?
Maybe a search, or a series of checkboxes… but I couldn't think of a good way to build a picker with so many options.
I wasn't expecting the idea to go any further.

Then I found [Choices.js], which has a bunch of tools for customising text boxes and selections in web forms.
I played with [the demo], and halfway down the page I found exactly what I was looking for – a picker that lets you select multiple inputs from a fixed list.
All the hard work is done for me, and I just need to provide a list of choices.

TransportAPI is good for looking up stations one-by-one, but I couldn't find a way to dump a complete list of stations.
Looking around, I found that Trainline (the ticketing company) publish [a list of stations], so I wrote a Python script that grabs their data and pulls out the latitude/longitude coordinates.
Trainline only have England and Wales, so I topped it up with data for Ireland and Northern Ireland [from Wikipedia].
I can feed this data into Choices.js to populate the picker.

So, to recap, I'm using:

*   OpenStreetMap for the map tiles
*   Leaflet.js to render the map and the markers for each station
*   A mixture of TransportAPI, Trainline and Wikipedia to get the lat/long coordinates for each station
*   Choices.js to let a user choose from the list of stations

Putting it all together, this is what the app looks like:

<img src="/images/2020/uk_stations_map_1x.png" srcset="/images/2020/uk_stations_map_1x.png 1x, /images/2020/uk_stations_map_2x.png 2x" alt="Screenshot of an app. Most of the app is a grayscale map of the UK with green circles dotted all over it, and below it is a text field with a list of station names in green bubbles.">

A map tells you much more than a flat list:

-   There's a big cluster of stations around London (where I work) and Hertfordshire (where I live).
-   There's a smaller cluster near Gloucestershire, where I grew up.
-   Looking further afield, you can tell I haven't really ventured north by train.
    But you can see my holidays to Leeds and Edinburgh, and you can just about spot the two stations I visited on my [day trip to the Forth Bridge][Forth]!

The app isn't wonderfully fast – it preloads all the station data as a JSON blob, and that takes time to download and render.
I'm sure it could be made faster, but this was only a bit of fun, and not something I want to sink lots of time into.

If you want to play with it yourself, it's at <https://uk-stations-map.glitch.me/>, or the code is [on GitHub].

[Letchworth Garden City]: https://en.wikipedia.org/wiki/Letchworth_Garden_City_railway_station
[Leaflet.js]: https://leafletjs.com/
[OpenStreetMap]: https://www.openstreetmap.org/
[TransportAPI]: https://www.transportapi.com/
[Choices.js]: https://github.com/jshjohnson/Choices
[the demo]: https://joshuajohnson.co.uk/Choices/
[a list of stations]: https://github.com/trainline-eu/stations
[from Wikipedia]: https://en.wikipedia.org/wiki/List_of_railway_stations_in_Ireland
[Forth]: /2019/03/forth-bridge/
[on GitHub]: https://github.com/alexwlchan/uk-station-map
