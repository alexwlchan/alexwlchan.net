---
layout: post
date: 2024-02-11 23:04:30 +0000
title: Moving my YouTube Likes from one account to another
summary: Some experimenting with the YouTube API to merge two accounts into one.
tags:
  - python
  - youtube
colors:
  index_light: "#ff0000"
  index_dark:  "#ff4242"
---
I used to have two YouTube accounts, and I wanted to consolidate them into one.

I had two accounts as a way to keep two separate watch histories.
I was watching videos about gender and trans stuff before I came out, and I didn't want them appearing in my main account -- say, when I was listening to music at work.
That's less of a concern now than it was five or six years ago, and the lines between them have become blurry.
I don't need two accounts any more.

Because I only use YouTube for watching videos, and not posting, there were only three lists I really wanted to keep: my subscriptions, my Watch Later queue, and my Likes.
My subs and watch later were both small enough to copy by hand; the likes were the hard bit – I had about 1500 or so.

There's no built-in way to move Likes between YouTube accounts, so it was time to break out the YouTube API.

## Getting authentication working

The first step was getting some API credentials.
This uses the Google Cloud console, which I'm not super familiar with, but YouTube has a lot of quickstart guides and code samples which made the process much easier.

I used the [Python quickstart guide][quickstart_guide], and went through the following steps:

1.  Create a project in the Google Cloud console
2.  Enable the YouTube Data API for that project
3.  Create some OAuth credentials, which came in a JSON file I had to download

At some point during this process, I had to create an OAuth consent screen.
If I was publishing this app for the world to use, you'd see this as signing into the app, and it would have to be reviewed by Google.
Because I was only writing scripts for me, I was able to mostly skip this step -- I left the app with a "testing" status, and just listed my two YouTube accounts as "test users":

{%
  picture
  filename="google-cloud-oauth-consent.png"
  alt="Screenshot of a settings screen in Google Cloud console. The panel is a titled ‘OAuth consent screen’, and there’s a table labelled ‘Test users’. It has two rows with redacted email addresses, and buttons to add/remove users from the table."
  width="546"
  class="screenshot"
%}

After this, I tried to run the [sample Python script][sample_script] from Google's documentation.
It didn't work -- it was written for an older version of the Python libraries.
In particular, it used `flow.run_console()`, which uses an authentication method which has been deprecated for over a year.
A [Stack Overflow answer][so_answer] suggested I use `flow.run_local_server()`, and that was more successful.

Here's the first script I got working, which is a modified version of the sample code:

```python
import googleapiclient.discovery  # pip install google-api-python-client==1.7.2
import google_auth_oauthlib.flow  # pip install google-auth-oauthlib==0.4.1


def create_youtube_client(client_secrets_file):
    """
    Given the path to a JSON file with OAuth credentials from the
    Google Cloud console, create an authenticated client.
    """
    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
    )
    credentials = flow.run_local_server()

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    return youtube


if __name__ == "__main__":
    youtube = create_youtube_client(
        client_secrets_file="client_secret_12345.apps.googleusercontent.com.json"
    )

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()

    from pprint import pprint; pprint(response)
```

When I run this, the script kicks me out into a web browser, where I have to go through the usual Google login screen, and confirm I want to use this app.
After I clicked through a few confirmation screens, my browser eventually got to a page that said:

```
The authentication flow has completed. You may close this window.
```

and back in my terminal window, the script was running and printing a list of my playlists.

Already this was further than I'd got in the past -- I had an authenticated API client, and it was retrieving real data from my YouTube account.
Good progress!

[quickstart_guide]: https://developers.google.com/youtube/v3/quickstart/python
[sample_script]: https://developers.google.com/youtube/v3/docs/channels/list?apix=true
[so_answer]: https://stackoverflow.com/a/74834470/1558022

## Making the authentication better

The authentication code above works, but it has two major issues:

*   It's reading my OAuth client config from a JSON file on disk.
    Credentials should never be stored in plain text, so I want to put that somewhere more secure.

*   It doesn't remember the credentials from `flow.run_local_server()` -- every time I run the script, I have to go through the in-browser authentication flow.
    I was running the script many times as I gradually built up the code, and this quickly got annoying.

Both of these issues can be solved using the [keyring module][keyring], which provides a platform-agnostic interface to the system password store (in my case, the login keychain on macOS).

I changed the function to fetch the OAuth client config from the keychain, and to store retrieved credentials in the keychain.
When I run it repeatedly, it retrieves the stored credentials rather than sending me back through the in-browser flow.

After running these scripts for a while, I discovered that Google's OAuth credentials expire after about a week.
I wrote some rudimentary code to handle credential expiry -- it deletes the stored credentials, and sends me back through the in-browser flow.
There are almost certainly better ways to do this, but my simplistic approach worked well enough for my one-off script.

Here's my updated function:

```python
import datetime
import json

import google.oauth2.credentials
import googleapiclient.discovery  # pip install google-api-python-client==1.7.2
import google_auth_oauthlib.flow  # pip install google-auth-oauthlib==0.4.1
import keyring


def create_youtube_client(label: str):
    """
    Get an authenticated OAuth client for YouTube.

    It gets the OAuth config from the system keychain, and caches
    per-user credentials in the keychain under ("youtube", label).
    """
    api_service_name = "youtube"
    api_version = "v3"
    scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Try to retrieve a stored OAuth access token from the keychain.
    #
    # This saves me going through the in-browser authentication flow
    # if I've already run the script.
    stored_credentials = keyring.get_password("youtube", label)

    if stored_credentials is not None:
        json_credentials = json.loads(stored_credentials)

        if "expiry" in json_credentials:
            expiry = datetime.datetime.fromisoformat(json_credentials["expiry"])
            expiry = expiry.replace(tzinfo=None)
            json_credentials["expiry"] = expir

        credentials = google.oauth2.credentials.Credentials(**json_credentials)

    # If there are no stored credentials, fetch new ones.
    else:
        # Retrieve the OAuth client credentials from the keychain.
        #
        # This contains the contents of the JSON file that I downloaded
        # from the Google Cloud console, but now those credentials aren't
        # just saved as a plaintext file on disk.
        stored_client_secrets = keyring.get_password("youtube", "client_secrets")
        if stored_client_secrets is None:
            raise ValueError("Could not find OAuth client secrets in keychain!")

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
            client_config=json.loads(stored_client_secrets), scopes=scopes
        )
        credentials = flow.run_local_server()

        # Save these credentials in the system keychain, so they can be
        # retrieved later.
        keyring.set_password("youtube", label, credentials.to_json())

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    # The OAuth credentials don't last forever -- they seem to expire after
    # a week.  This is a slightly ropey attempt to work around that.
    #
    # If we call the API and the saved token is expired, just delete
    # it and get new creds -- sending me back through the in-browser flow.
    #
    # Notes:
    #
    #   - There are ways to refresh OAuth tokens that don't involve
    #     sending me back through the in-browser flow, but I didn't
    #     look at them as part of this project.
    #   - Catching all exceptions is a bit broad.  This code should really
    #     retry only if it gets a "credentials expired" exception, and
    #     throw any other exceptions immediately.
    #
    try:
        request = youtube.channels().list(part="snippet", mine=True)
        request.execute()
    except Exception as e:
        keyring.delete_password("youtube", label)
        return create_youtube_client(label)
    else:
        return youtube
```

This function is more complicated than Google's sample code, and there are more ways that it could be improved.
Authentication is hard!

[keyring]: https://pypi.org/project/keyring/

## Actually using the YouTube API

With an authenticated client, it was relatively straightforward to write code that interacts with YouTube's APIs.
I've lost the links, but I found snippets of sample code in Google's documentation that I was able to adapt.

I started by wrapping the `create_youtube_client` in a class, and writing a function to list all the videos I'd liked:

```python
class YouTubeClient:
    def __init__(self, label: str):
        self.youtube = self.create_youtube_client(label)

    def create_youtube_client(self, label: str):
        …

    def get_liked_videos(self):
        """
        Generate a list of videos that this YouTube account has liked.
        """
        kwargs = {"part": "snippet", "playlistId": "LL", "maxResults": "50"}

        while True:
            request = self.youtube.playlistItems().list(**kwargs)
            response = request.execute()

            yield from response["items"]

            try:
                kwargs["pageToken"] = response["nextPageToken"]
            except KeyError:
                break
```

[**Edit, 15 February 2024:** the original version of this code called the `videos()` endpoint and filtered for my likes, but that was only able to see the first 1000 likes. That was fine for this project, where I was gradually deleting the list, but not in general. I've changed it to use the `playlistItems()` API, which seems to return the full set.]

This generates videos in reverse order of liking them -- the most recently liked video comes first.
The items are large dicts which include various metadata fields about each video, of which the most interesting one to me is the ID:

````python
{'id': 'J-u2aW7T2bw', …}
{'id': 'XPaKAh2zxgk', …}
{'id': '-q7ZVXOU3kM', …}
```

Then I wrote a couple of methods which like/unlike a video.
Because these are modifying data in YouTube, I had to change the `scopes` to `https://www.googleapis.com/auth/youtube`, replacing the `youtube.readonly` scope I'd been using previously.

```python
class YouTubeClient:
    …

    def like_video(self, *, video_id):
        """
        Mark a video as "liked" on YouTube.
        """
        request = self.youtube.videos().rate(id=video_id, rating="like")
        response = request.execute()

    def unlike_video(self, *, video_id):
        """
        Remove the "liked" rating from a video on YouTube.
        """
        request = self.youtube.videos().rate(id=video_id, rating="none")
        response = request.execute()
```

Putting these functions together, I was then able to write a short script which moved my likes from one account to the other:

```python
old_youtube = YouTubeClient(label="old_account")
new_youtube = YouTubeClient(label="new_account")

for video in old_youtube.get_liked_videos():
    video_id = video["id"]

    print("https://www.youtube.com/watch?v={video_id}")
    new_youtube.like_video(video_id=video_id)
    old_youtube.unlike_video(video_id=video_id)
```

Removing the likes from the old account wasn't strictly necessary -- I was planning to close the account when I was done -- but it was an easy way to track the progress, and turned out to be helpful towards the end of the process (more on that below).

Incidentally, around the time I wrote this code, David published a post about [writing good programming abstractions], and I think this is a nice example of one.
Wrapping these API calls in a couple of named functions doesn't do anything to help de-duplication, but it does make the intent of the final script much clearer.

[writing good programming abstractions]: https://notebook.drmaciver.com/posts/2024-01-13-08:28.html

## Running the code in practice

By and large this code worked extremely well.
Almost all of the videos moved across seamlessly, and I could watch it in two side-by-side browser windows -- likes appeared in one account as they disappeared from the other.
It was substantially quicker and easier than if I'd tried to do it by hand.

I did run into a couple of non-obvious issues:

*   The YouTube API has a quota, and I burnt through it pretty quickly.
    You get 10,000 units per day, and rating a video (aka like/unlike) [costs 50 units][table].
    I had to make two calls to move each video (one like, one unlike), so I could only move about 100 videos a day.

    The quota resets at midnight Pacific Time, or about 8am in London.
    I got into the habit of running the script once a day, every day, until I'd moved my entire list of Liked videos.
    It took a while, but still less than doing it by hand!

    You can apply for a quota increase, but I didn't bother -- I knew I'd only run into the quota a handful of times, and it was easier to spread my runs over multiple days than fill in an application for more quota.
    The docs say it can take a week or so to approve quota increases, by which I'd probably be done.

*   Sometimes I'd get a 403 error with the message *"The owner of the video that you are trying to rate has disabled ratings for that video"*.

    I'm not sure what this means -- if I opened the video in my web browser, I could still use the like/unlike buttons.
    This only affected a handful of videos in my entire list, so I just used my web browser to move them across.

*   The API couldn't see the last dozen or so videos.
    On the last day of running the script, the `get_liked_videos()` function returned an empty list, but I could still see some liked videos in the old account in my web browser.
    I'm not sure why they were invisible to the API.

    Again, because it was only a handful of videos, I moved them across by hand.

    [**Edit, 15 February 2024:** I think this was caused by my use of the `videos()` API instead of `playlistItems()`; see above.]

These were relatively minor issues, and easy to work around.
And once I'd finished running this script, I was able to close the old account and throw away this code -- but maybe I'll come back to these notes if I have another interesting idea for using the YouTube API.

[table]: https://developers.google.com/youtube/v3/determine_quota_cost
