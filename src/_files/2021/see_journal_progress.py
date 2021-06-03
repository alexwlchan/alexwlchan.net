#!/usr/bin/env python
"""
This script creates a coloured calendar view that highlights days when
I did/didn't write a journal entry.
"""

import calendar
import colorsys
import datetime
import glob
import itertools
import os
import random
import tempfile
import webbrowser


def get_file_paths_under(root):
    """Generates the paths to every file under ``root``."""
    if not os.path.isdir(root):
        raise ValueError(f"Cannot find files under non-existent directory: {root!r}")

    for dirpath, _, filenames in os.walk(root):
        for f in filenames:
            if os.path.isfile(os.path.join(dirpath, f)):
                yield os.path.join(dirpath, f)


def get_date_of_journal_entry(path):
    if not path.endswith(".md"):
        return

    try:
        # The first line of a file should be something like 'date: 2021-05-09'
        header = next(open(path))
        d = datetime.datetime.strptime(header.strip(), "date: %Y-%m-%d")
    except (StopIteration, ValueError):
        return
    else:
        return d.date()


class JournalCalendar(calendar.HTMLCalendar):
    def formatday(self, theyear, themonth, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return '<td id="day-%s-%02d-%02d" class="%s">&nbsp;</td>' % (
                theyear,
                themonth,
                day,
                self.cssclass_noday,
            )
        else:
            return '<td id="day-%s-%02d-%02d" class="%s">%d</td>' % (
                theyear,
                themonth,
                day,
                self.cssclasses[weekday],
                day,
            )

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        day_abbr = {
            0: "M",
            1: "Tu",
            2: "W",
            3: "Th",
            4: "F",
            5: "Sa",
            6: "Su",
        }
        return '<th class="%s">%s</th>' % (
            self.cssclasses_weekday_head[day],
            day_abbr[day],
        )

    def formatweek(self, theyear, themonth, theweek):
        """
        Return a complete week as a table row.
        """
        s = "".join(self.formatday(theyear, themonth, d, wd) for (d, wd) in theweek)
        return "<tr>%s</tr>" % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a(
            '<table border="0" cellpadding="0" cellspacing="0" class="%s">'
            % (self.cssclass_month)
        )
        a("\n")
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a("\n")
        a(self.formatweekheader())
        a("\n")
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(theyear, themonth, week))
            a("\n")
        a("</table>")
        a("\n")
        return "".join(v)


def render_calendar(dates):
    lines = ["<html><title>Journal progress</title>"]

    min_year = min(d.year for d in dates)

    today = datetime.date.today()
    yesterday = datetime.date.today() - datetime.timedelta(days=1)

    if max(dates) == today:
        lines.append("<p>You've already journalled today. Well done!</p>")
    elif max(dates) == yesterday:
        lines.append("<p>Your last journal entry was yesterday. Keep it up!</p>")
    else:
        lines.append("<p>Your last journal entry was %s.</p>" % max(dates).strftime("%d %m %Y"))

    streak = 0
    t = today if today in dates else yesterday
    while t in dates:
        streak += 1
        t -= datetime.timedelta(days=1)

    if streak == 0:
        lines.append("<p>You don't have a streak.</p>")
    else:
        lines.append("<p>Your current streak is %d day%s.</p>" % (streak, "s" if streak > 1 else ""))

    for year in range(today.year, min_year - 1, -1):
        lines.append(f'<div id="progress-{year}">')
        lines.append(JournalCalendar().formatyear(year, 6))

        by_year = {d: v for d, v in dates.items() if d.year == year}
        r = random.Random(year)
        hue = r.random()

        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

        try:
            max_by_year = max(by_year.values())
        except ValueError:
            pass

        lines.append("</div>")

        lines.append("<style>")

        lines.append(
            """#progress-%s {
                border: 2px solid rgb(%d, %d, %d);
                border-radius: 10px;
                margin-bottom: 1em;
            }"""
            % (year, int(r * 255), int(g * 255), int(b * 255))
        )

        for d, v in by_year.items():
            lines.append(
                "#day-%s { background-color: rgba(%d, %d, %d, %.2f); }"
                % (
                    d.isoformat(),
                    int(r * 255),
                    int(g * 255),
                    int(b * 255),
                    v / max_by_year,
                )
            )

        lines.append("</style>")

    lines.append("<style>")

    t = datetime.date.today() + datetime.timedelta(days=1)
    while t.year == datetime.date.today().year:
        lines.append("#day-%s { color: #ddd; }" % t.isoformat())
        t += datetime.timedelta(days=1)

    lines.append(
        "td { padding: 1.5px; vertical-align: top; text-align: center; font-size: 80%; }"
    )
    lines.append("table { margin: 5px;  }")
    lines.append('th[colspan="6"] { font-size: 150%; }')
    lines.append("div { text-align: center;  padding: 5px;}")
    lines.append(
        "th.mon, th.tue, th.wed, th.thu, th.fri, th.sat, th.sun { font-size: 65%; }"
    )
    lines.append(
        "body { max-width: 835px; margin-left: auto; margin-right: auto; font: 11pt sans-serif; }"
    )
    lines.append(
        "p { font-size: 150%; text-align: center; margin: 1em; }"
    )
    lines.append("</style>")

    return "\n".join(lines)


if __name__ == "__main__":
    dates = {
        get_date_of_journal_entry(f): os.stat(f).st_size
        for f in get_file_paths_under(".")
    }

    del dates[None]

    _, out_path = tempfile.mkstemp(suffix=".html")
    with open(out_path, "w") as out_file:
        out_file.write(render_calendar(dates))

    webbrowser.open(f"file://{out_path}")
