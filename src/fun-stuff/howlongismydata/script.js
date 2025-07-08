function recompute() {
  var value = document.getElementById("value").value;
  var unit = document.getElementById("unit").value;

  if (unit == "EB") {
    document.getElementById("reaction").innerHTML = "🤯";
  } else {
    document.getElementById("reaction").innerHTML = "";
  }

  if (value == "") {
    return;
  }

  if (unit == "MB") {
    var totalMegabytes = value;
  } else if (unit == "GB") {
    var totalMegabytes = 1024 * value;
  } else if (unit == "TB") {
    var totalMegabytes = 1024 * 1024 * value;
  } else if (unit == "PB") {
    var totalMegabytes = 1024 * 1024 * 1024 * value;
  } else if (unit == "EB") {
    var totalMegabytes = 1024 * 1024 * 1024 * 1024 * value;
  }

  // A floppy disk can hold 1.44MB of data
  var floppyDiskCount = totalMegabytes / 1.44;

  // The height of a floppy disk is ~3.3mm.  Rememeber we can't have
  // partial floppy
  var heightInMillimetres = Math.ceil(floppyDiskCount) * 3.3;

  var metricHeight = getMetricDisplayHeight(heightInMillimetres);
  var imperialHeight = getImperialDisplayHeight(heightInMillimetres);

  document.getElementById("results").innerHTML = "This much data would need <span class=\"displayHeight\">" + metricHeight + "</span> (or <span class=\"displayHeight\">" + imperialHeight + "</span>) of shelving."
}

function getMetricDisplayHeight(heightInMillimetres) {
  if (heightInMillimetres < 10) {
    return heightInMillimetres + "&nbsp;" + "mm";
  }

  var heightInCentimetres = heightInMillimetres / 10;
  if (heightInCentimetres < 100) {
    return heightInCentimetres + "&nbsp;" + "cm";
  }

  var heightInMetres = Math.round(heightInCentimetres / 10) / 10;
  if (heightInMetres < 1000) {
    return heightInMetres + "&nbsp;" + "m";
  }

  var heightInKilometres = Math.round(heightInMetres / 100) / 10;
  return numberWithCommas(heightInKilometres) + "&nbsp;" + "km";
}

function getImperialDisplayHeight(heightInMillimetres) {
  // one inch = 2.54 cm
  var millimetresPerInch = 25.4;

  // one foot = 12 inches
  var millimetresPerFoot = millimetresPerInch * 12;

  // one yard = 3 feet
  var millimetresPerYard = millimetresPerFoot * 3;

  // one mile = 1760 yards
  var millimetresPerMile = millimetresPerYard * 1760;

  if (heightInMillimetres < millimetresPerFoot) {
    return Math.round(heightInMillimetres / millimetresPerInch * 100) / 100 + "&nbsp;" + "in";
  }

  if (heightInMillimetres < millimetresPerYard) {
    var feet = Math.floor(heightInMillimetres / millimetresPerFoot);
    var inches = Math.round((heightInMillimetres % millimetresPerFoot) / millimetresPerInch);
    return feet + "&nbsp;" + "ft " + inches + "&nbsp;" + "in";
  }

  if (heightInMillimetres < millimetresPerMile) {
    return Math.round(heightInMillimetres / millimetresPerYard * 10) / 10 + "&nbsp;" + "yards";
  }

  var heightInMiles = Math.round(heightInMillimetres / millimetresPerMile * 10) / 10;
  return numberWithCommas(heightInMiles) + "&nbsp;" + "miles";
}

// https://stackoverflow.com/a/2901298/1558022
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}