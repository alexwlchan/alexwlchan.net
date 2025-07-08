L.TileLayer.Grayscale = L.TileLayer.extend({
	options: {
		quotaRed: 21,
		quotaGreen: 71,
		quotaBlue: 8,
		quotaDividerTune: 0,
		quotaDivider: function() {
			return this.quotaRed + this.quotaGreen + this.quotaBlue + this.quotaDividerTune;
		}
	},

	initialize: function (url, options) {
		options = options || {}
    options.crossOrigin = true;
		L.TileLayer.prototype.initialize.call(this, url, options);

		this.on('tileload', function(e) {
			this._makeGrayscale(e.tile);
		});
	},

	_createTile: function () {
		var tile = L.TileLayer.prototype._createTile.call(this);
    tile.crossOrigin = "Anonymous";
		return tile;
	},

	_makeGrayscale: function (img) {
		if (img.getAttribute('data-grayscaled'))
			return;

    img.crossOrigin = '';
		var canvas = document.createElement("canvas");
		canvas.width = img.width;
		canvas.height = img.height;
		var ctx = canvas.getContext("2d");
		ctx.drawImage(img, 0, 0);

		var imgd = ctx.getImageData(0, 0, canvas.width, canvas.height);
		var pix = imgd.data;
		for (var i = 0, n = pix.length; i < n; i += 4) {
                        pix[i] = pix[i + 1] = pix[i + 2] = (this.options.quotaRed * pix[i] + this.options.quotaGreen * pix[i + 1] + this.options.quotaBlue * pix[i + 2]) / this.options.quotaDivider();
		}
		ctx.putImageData(imgd, 0, 0);
		img.setAttribute('data-grayscaled', true);
		img.src = canvas.toDataURL();
	}
});

class MapManager {
  constructor(div_id) {
    this.map = L.map(div_id);
    this.addOpenstreetMapTiles();

    this.markerCache = {};
  }

  addOpenstreetMapTiles() {
    this.map.setView([54.505, -4.5], 6);

    new L.TileLayer.Grayscale('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, station data from <a href="https://github.com/trainline-eu/stations">Trainline EU</a> and <a href="https://en.wikipedia.org/wiki/List_of_railway_stations_in_Ireland">Wikipedia</a>',
    }).addTo(this.map);
  }

  addMarker(label, long, lat) {
    const marker = L.circleMarker([lat, long], {
      fill: true,
      color: '#0b9e00',
      fillColor: 'rgba(11, 158, 0, 0.3)',
      radius: 5,
    }).addTo(this.map);

    this.markerCache[label] = marker;
  }

  removeMarker(label) {
    this.map.removeLayer(this.markerCache[label]);
    delete this.markerCache[label];
  }
}

// Keep track of the stations a user has selected in their local storage.
//
// Local storage is persistent across sessions, so when they return to the
// app, it should remember the stations they've selected.
//
// The stations are stored as a semicolon-separated string, e.g.
//
//      Cardiff Bay;London Victoria;Cosham
//
// It assumes station names are stable across time, which seems reasonable.
// If a station is deleted, we might fail to unpack that station name later.
//
class StateManager {
  constructor(stations) {
    this.stations = stations;
    this.selected = [];
  }

  updateCounter() {
    if (this.selected.length === 1) {
      var text = "You&rsquo;ve visited <strong>1</strong> station!";
    } else if (this.selected.length === 0) {
      var text = "You haven&rsquo;t visited any stations yet!";
    } else {
      var text = "You&rsquo;ve visited <strong>" + this.selected.length + "</strong> stations!";
    }

    document.getElementById("counter").innerHTML = text;
  }

  addStation(stationName) {
    this.selected.push(stationName);
    window.localStorage.setItem("stations", this.selected.join(";"));
    this.updateCounter();
  }

  removeStation(stationName) {
    this.selected = this.selected.filter(station => station !== stationName);
    window.localStorage.setItem("stations", this.selected.join(";"));
    this.updateCounter();
  }
}

// Manages the <select> where the user picks the stations they've visited.
//
// This sets up an instance of Choices.js based on the "multiple select input"
// example from https://github.com/jshjohnson/Choices
//
// It is also responsible for notifying the map/local storage when the user
// adds or removes the station.
class PickerManager {
  constructor(pickerId, mapManager, stateManager, stations) {
    this.element = document.getElementById(pickerId);

    this.createChoices(stateManager);
    this.setupEventListeners(mapManager, stateManager, stations);
  }

  // When the app starts, we display a random selection of stations to illustrate
  // how the map works.
  //
  // However, if the user has used the app before, we want to track that -- and
  // restore the stations they've already set, not overwrite them with new ones.
  //
  // We use the `hasEdits` field to track whether the user has ever edited the
  // list of stations.
  hasUserEdits() {
    return (
      window.localStorage.getItem("hasEdits") === "true" &&
      window.localStorage.getItem("stations") !== null &&
      window.localStorage.getItem("stations") !== ""
    )
  }

  createChoices(stateManager) {
    const choices = [];
    for (var name in stations) {
      var data = stations[name];
      choices.push({value: name, label: name});
    }

    const picker = new Choices(this.element, {
      removeItemButton: true,
      choices: choices,
    });

    const items = [];

    if (this.hasUserEdits()) {
      var stationNames = window.localStorage.getItem("stations").split(";");
    } else {
      // If this is a first run, pick a random selection of stations
      // to illustrate the principle.  Choose an integer between 3 and 7,
      // then add that number of stations.
      var stationNames = [];
      const randomCount = Math.floor((Math.random() * 5) + 3);

      for (var i = 0; i < randomCount; i++) {
        var chosenStation = choices[Math.floor(Math.random() * choices.length)];

        var chosenName = chosenStation.label;
        stationNames.push(chosenName);
      }
    }

    for (var i = 0; i < stationNames.length; i++) {
      var stationName = stationNames[i];
      var stationCoords = stations[stationName];
      var longitude = stationCoords[0];
      var latitude = stationCoords[1];
      mapManager.addMarker(stationName, longitude, latitude);
      stateManager.addStation(stationName);
      items.push(stationName);
    }

    picker.setValue(items);
  }

  setupEventListeners(mapManager, stateManager, stations) {
    this.element.addEventListener(
      "addItem",
      function(event) {
        window.localStorage.setItem("hasEdits", true);

        var stationName = event.detail.label;
        var stationCoords = stations[stationName];
        var longitude = stationCoords[0];
        var latitude = stationCoords[1];
        mapManager.addMarker(stationName, longitude, latitude);
        stateManager.addStation(stationName);
      },
      false,
    )

    this.element.addEventListener(
      "removeItem",
      function(event) {
        window.localStorage.setItem("hasEdits", true);

        var stationName = event.detail.label;
        mapManager.removeMarker(stationName);
        stateManager.removeStation(stationName);
      },
      false,
    )
  }
}
