---
layout: til
title: Use the IMAGE function to insert an image into a spreadsheet
date: 2024-01-09 12:17:28 +00:00
tags:
  - spreadsheets
---
There's an `IMAGE` function in both [Google Sheets] and [Microsoft Excel] that you can use to insert images into cells, in particular from URLs:

```
IMAGE("https://www.google.com/images/srpr/logo3w.png")
```

I used this when we had a list of Flickr URLs with photos that we wanted to review visually -- I added a new column with URLs pointing to the raw JPEGs, and then I used the `IMAGE` formula to display thumbnail photos inline.

[Google Sheets]: https://support.google.com/docs/answer/3093333
[Microsoft Excel]: https://support.microsoft.com/en-us/office/image-function-7e112975-5e52-4f2a-b9da-1d913d51f5d5