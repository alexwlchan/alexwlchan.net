#!/usr/bin/env python3

import json

if __name__ == "__main__":
    with open("alt_text.json", "w") as outfile:
        for i, line in enumerate(open("tweets.json")):
            tweet = json.loads(line)

            new_line = {"id": tweet["id_str"], "media": []}

            for media in tweet["extended_entities"]["media"]:
                new_line["media"].append(
                    {
                        "alt_text": media["ext_alt_text"],
                        "display_url": media["display_url"],
                        "media_url": media["media_url_https"],
                    }
                )

            outfile.write(json.dumps(new_line) + "\n")
