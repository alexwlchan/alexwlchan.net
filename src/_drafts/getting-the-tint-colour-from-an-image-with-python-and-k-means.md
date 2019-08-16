---
layout: post
title: Getting a tint colour from an image with Python and k-means
summary:
category: Programming and code
---

As [part of my app][docstore] for managing my electronic documents, there's a grid view that displays big thumbnails of all my files.
If I'm looking for something with a distinctive thumbnail (say, an ebook cover), I can easily skim a grid of thumbnails to find it.
(I talked about how I create the PDF thumbnails in [a separate post][thumbnails].)

When you hover over a card, it shows a little panel with some details about the file: when I saved it, what tags I've assigned, and the source URL.
Here's a screenshot:

<img src="/images/2019/docstore_card_view.jpg" style="width: 600px;" alt="Left: a red and yellow book cover with the words “Bled in Slovenian folk tales, by Dusica Kunaver”. Right: the same cover, with a portion of white and some metadata covering the bottom half of the book. A black arrow from the left to right image.">

The source URL and tags are both clickable links.
I can go back to the page where I downloaded a file from, or find other files with similar tags.

It's a bit visually jarring to see the [Bootstrap blue][bootstrap] next to the large thumbnail.
I wanted to see if I could pick a tint colour from the thumbnail, and use that for the link colour -- for example, taking the bright red sash from the book cover above.

<img src="/images/2019/docstore_card_view_red.jpg" style="width: 600px;" alt="The same card view above, but now the blue links are in red.">

I've come up with an approach that seems to work fairly well, which uses [k-means clustering][k_means] to get the dominant images, and then compares the contrast with white to pick the best colour to use as the tint.
I've tried my code with a few thousand images, and it picks reasonable colours each time -- not always optimal, but scanning the list I didn't see anything wildly inappropriate or unusable.

Reader beware: I'm not a data scientist, and this isn't my speciality.
This code works for my personal project, but you might want to double-check it before using it for anything bigger.

[docstore]: https://github.com/alexwlchan/docstore
[thumbnails]: /2019/07/creating-preview-thumbnails-of-pdf-documents/
[bootstrap]: https://getbootstrap.com
[k_means]: https://en.wikipedia.org/wiki/K-means_clustering



## Idea 1: Find the most common colour in an image

My first thought was to try a very simple approach: tally all the colours used in the image, and pick the colour that appears most often.

The Pillow library has [get_colors() method][get_colors] that lets you get a list of all the colours in an image, along with their frequency.
So we can find the most common colour like so:

```python
import collections

from PIL import Image


def get_colors_by_frequency(im):
    maxcolors = im.width * im.height
    colors = im.getcolors(maxcolors=maxcolors)
    return collections.Counter({color: count for count, color in colors})


if __name__ == "__main__":
    im = Image.open("cats.jpg")
    colors = get_colors_by_frequency(im)
    print(colors.most_common(1))
```

But if you actually try this, you quickly discover that it usually returns something close to black or close to white -- it's not very representative!
Here's an example:

<img src="/images/2019/green_chair.jpg" style="width: 600px;">

A human looking at that photo would probably pick green as the main colour -- but there are lots of different shades of green.
Although there are more green pixels than any other colour, there are only a few pixels of each shade, so they're low down on the colour tally.

If we want to extract the main colours, we need to be able to group similar-looking colours together.

I played with a couple of simple ideas, but I didn't get anywhere useful, so I searched for other people tackling this problem.
I found [a post by Charles Leifer][leifer] addressing a similar problem that suggested using [k-means clustering][k_means], so I decided to try that.

I've never used k-means before, so I wanted to take time to understand it.
There's an implementation of k-means [in scikit-learn][sklearn], but I wanted to write my own to be sure I really knew what was going on.
If you already know how k-means works, you can skip the next two sections -- if not, read on, and I'll do my best to explain.

[get_colors]: https://pillow.readthedocs.io/en/stable/reference/Image.html?highlight=getcolors#PIL.Image.Image.getcolors
[k_means]: https://en.wikipedia.org/wiki/K-means_clustering
[leifer]: http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/
[sklearn]: https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html



## What is k-means clustering?

Suppose we have a collection of data points.
*Clustering* means dividing the data points into different groups, so all of the points in the same group are similar in some way.
(And conversely, points in different groups should be different.)

Let's suppose our data points are positions on a 2D plane.
If we group them into three clusters by saying "points that are close together are similar", we might end up with this clustering:

<figure style="width: 400px;">
  <img src="/images/2019/cluster_analysis.svg">
  <figcaption>
    The squares are coloured differently to show which cluster they're in.
    Illustration from <a href="https://en.wikipedia.org/wiki/File:Cluster-2.svg">Wikimedia Commons</a>.
  </figcaption>
</figure>


