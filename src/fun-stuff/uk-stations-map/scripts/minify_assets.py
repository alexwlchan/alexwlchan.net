#!/usr/bin/env python

import glob

import cssmin
import jsmin


if __name__ == "__main__":
    css_strings = []

    for css_path in sorted(glob.glob("assets/*.css")):
        css_strings.append(cssmin.cssmin(open(css_path).read()))

    with open("static/stations.min.css", "w") as out_file:
        out_file.write("\n".join(css_strings))

    js_strings = []

    for js_path in sorted(glob.glob("assets/*.js")):
        js_strings.append(jsmin.jsmin(open(js_path).read()))

    with open("static/stations.min.js", "w") as out_file:
        out_file.write("\n".join(js_strings))
