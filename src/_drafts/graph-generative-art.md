---
layout: post
title: Generating art from lattice graphs
summary: Randomly selecting a subset of edge from a graph can make pretty pictures.
tags: generative-art
theme:
  card_type: summary_large_image
  image: /images/2022/graph_gen_art_card.png
---

<style>
  /*
    By default, this is a grid that's four columns wide, but on narrow screens
    (i.e. mobile), I shrink it to two columns so it remains readable.

    I think I might do a checkerboard pattern on the 4-wide layout, and I want
    to retain that on the 2-wide layout, so I need to swap the 3rd/4th in every row.

    e.g. if I have

        X1 .2 X3 .4
        .5 X6 .7 X8

    then on the mobile layout I want

        X1 .2
        .4 X3
        X6 .5
        .7 X8

    I swap the orders with `grid-column` properties, then the `grid-auto-flow`
    stops there being gaps in the grid.
  */
  .grid_4up {
    max-width: 650px;
    margin-left:  auto;
    margin-right: auto;
    display: grid;
    grid-gap: 8px;
    grid-template-columns: auto auto auto auto;
  }

  .grid_4up a {
    line-height: 0;
  }

  .grid_4up svg {
    max-width: 100%;
  }

  @media screen and (max-width: 500px) {
    .checkerboard {
      grid-template-columns: auto auto;
      grid-auto-flow: dense;
    }

    .checkerboard svg:nth-child(4n+3),
    .checkerboard svg:nth-child(8n+5) {
      grid-column: 2 / 2;
    }

    .checkerboard svg:nth-child(4n),
    .checkerboard svg:nth-child(8n+6) {
      grid-column: 1 / 2;
    }
  }
</style>

A couple of weeks ago, I went to see my sister playing percussion in a brass band [at the Proms][late_prom].
While I was on the train home, I had an idea for a fun art project.
I sketched it out on a napkin, got it working, posted a few pictures on Twitter, then ran out of time.

Today I'm sitting in the foyer of the Birmingham Symphony Hall, ready to watch her play in another band at [the British Open][open].
While I'm waiting for her to start, I have some time to revisit those ideas, and write them up properly.

(There's a lesson here about how art begets more art.)

These are a few of the pictures I was able to make:

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/brown_char_1.svg">
    {% inline_svg "_images/2022/graph-art/brown_char_1.svg" %}
  </a>
  <a href="/images/2022/graph-art/lime_circles.svg">
    {% inline_svg "_images/2022/graph-art/lime_circles.svg" %}
  </a>
  <a href="images/2022/graph-art/purple_diamond.svg">
    {% inline_svg "_images/2022/graph-art/purple_diamond.svg" %}
  </a>
  <a href="images/2022/graph-art/yellow_keyhole.svg">
    {% inline_svg "_images/2022/graph-art/yellow_keyhole.svg" %}
  </a>
  <a href="images/2022/graph-art/blue_circle_quadrants.svg">
    {% inline_svg "_images/2022/graph-art/blue_circle_quadrants.svg" %}
  </a>
  <a href="images/2022/graph-art/cream_clock.svg">
    {% inline_svg "_images/2022/graph-art/cream_clock.svg" %}
  </a>
  <a href="images/2022/graph-art/red_nuclear.svg">
    {% inline_svg "_images/2022/graph-art/red_nuclear.svg" %}
  </a>
  <a href="images/2022/graph-art/green_octagon.svg">
    {% inline_svg "_images/2022/graph-art/green_octagon.svg" %}
  </a>
</div>

In this post, I'm going to explain my ideas and thinking, and share the code I used to make them.

[late_prom]: https://www.theguardian.com/music/2022/aug/13/bbc-proms-30-32-tredegar-band-review-hms-pinafore-opera-holland-park-ohp-poulenc-double-bill-glyndebourne
[open]: https://www.4barsrest.com/news/54320/bands-ready-for-british-open-return



## The basic idea

In maths, a *graph* is a structure made up of vertices and edges.
Here's a simple example:

<figure style="width: 300px; margin-top: -1em; margin-bottom: -1em;">
  {% inline_svg "_images/2020/complex_graph.svg" %}
</figure>

My idea was to start with a graph and delete a random subset of edges.
(In particular, I'm assigning random weights to edges then finding a minimal spanning tree.
This gets a graph where all the edges are connected, but there are no loops.)

If I picked starting graphs with a certain structure, I thought I could get some fun pictures.

I used the [networkx Python library][networkx] to do all the graph logic, then I wrote my own template logic to render the graphs as SVGs.
All the images are inline SVGs, so you can right click and "View source" to see how they're drawn.
I'll link to the code at the end of the post.

[networkx]: https://networkx.org/



## Input graph #1: a square lattice

My initial napkin sketch had a [square lattice].
These are some of the pictures I was able to make:

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/Wed%2010%20Aug%202022%2006:17:49%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/Wed%2010%20Aug%202022%2006:17:56%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/Wed%2010%20Aug%202022%2006:17:59%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/Wed%2010%20Aug%202022%2006:18:12%20BST.svg">

When I shared them on Twitter, somebody compared them to the characters of a [conlang ("constructed language")][conlang].
I quite liked the comparison, so I drew another batch with an earthy brown and varying stroke widths:

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.6%202.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.8%202.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.4%202.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.5%202.svg">

To me, this second set feels vaguely evocative of Chinese characters.

[conlang]: https://en.wikipedia.org/wiki/Constructed_language
[square lattice]: https://en.wikipedia.org/wiki/Square_lattice



## Input graph #2: triangular lattice

I drew my square lattices using a networkx function called `grid_2d_graph`; I tried a similar-sounding function called [`triangular_lattice_graph`][tri_lattice].

That gave me a set of patterns that felt evocative of creeping vines on a wall, so I coloured them green:

[tri_lattice]: https://networkx.org/documentation/stable/reference/generated/networkx.generators.lattice.triangular_lattice_graph.html?highlight=triangular+lattice#networkx.generators.lattice.triangular_lattice_graph

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/vines.3.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/vines.2.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/vines.1.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/vines.0.svg">



## Input graph #3: radial lattice

I wanted to try using spiderweb-like diagrams as the input; I thought they'd look fun:

<img src="images/radial_lattice.png">

Initially I fixed the number of rings at 4, and let the number of spokes vary.
It took a bit more time to work out the bugs, but I really like the results.

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:14:00%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:14:36%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:14:35%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:18:00%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:23:14%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2012:54:14%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:22:49%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2007:23:17%20BST.svg">

Then I added even more randomness: varying the number of rings, the colour, and the stroke width.
These are a few of my favourites:

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.11.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.13.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.14.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:51:57%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.9.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.17.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:42:33%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:42:48%20BST.svg">

I especially like the blue hexagon, which feels like the topdown view of some sort of seafaring vessel.



## Input graph #4: radial lattice with curves

As you crank up the number of spokes in a radial lattice, it starts to approximate a circle -- so what if I could actually do proper curves in the lattice?
This took a bit more work, which ended up [as a separate post][curved_arcs].

Honourable mention to these image, which was created when I didn't set a `fill` attribute properly.
I didn't take this any further, but the opportunity for slices of a second colour feels like an interesting idea to explore.

<img src="https://spanning-tree-art.netlify.app/images/circle_Wed%2010%20Aug%202022%2006:53:08%20BST.svg">

Once I had the code for curves working, adding it to the radial lattice was fairly straightforward.
I had a lot of fun generating these images.
I also played with the idea of removing the central vertex, and having an "open" core.

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.10.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.12.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.8.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.16.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.46.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.7.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.36.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.57.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.3.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:51:48%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.50.svg">

These feel like designs out of science-fiction: the red circles feels evocative of radiation warnings, and several of them look like radar scanning screens (especially the teal).
As the spoke count increases, some of them feel like large mazes.
The thin yellow lines is one of my favourites, because it reminds me of a key hole.

[curved_arcs]: /2022/08/circle-party/



## Input graph #5: radial lattice with convave curves

For a final variation, I tried using concave curves in the lattice.
This matches the spider-web emoji, where the individual arcs bend towards the centre of the circle, rather than outward.

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.55.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.21.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.45.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.48.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.53.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:41:25%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:42:54%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:49:40%20BST.svg">

This got even more fun when I allowed arcs to bend alternately in and out, creating some extremely funky patterns.
(I think there are also a few images here where I mixed in code to randomly delete nodes in the input graphs, which is why there are a few gaps.)

<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.25.svg">
<img style="width: 150px; display: inline;" src="
https://spanning-tree-art.netlify.app/images/out.43.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.23.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:41:24%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:42:24%20BST.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.42.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out.22.svg">
<img style="width: 150px; display: inline;" src="https://spanning-tree-art.netlify.app/images/out_Thu%2011%20Aug%202022%2022:41:47%20BST.svg">

At one point I had this running in a background window, generating a new image every thirty seconds, which made for a fun bit of decoration.



## Further ideas

I have a bunch more thoughts for what I could do next, although I have no immediate plans to do so -- I proved the initial idea is workable, and I got some pretty pictures.
That's enough for now.

The only limit here is the graphs you start with: the stranger the input, the stranger the output.
Here I've worked exclusively with uniform lattice graphs, but this technique should be usable on any graph.

I did consider adding markers to the leaf nodes (the end of lines), to make them look more like traditional graph illustrations.

I mentioned earlier that some of the patterns look like the walls of a maze.
These wouldn't actually work as mazes, but it feels like this isn't too far from a maze generator.
Maybe if you used this to create the negative space, not the walls?

I made these with some scrappy Python scripts, using [networkx] for the graph algorithms and generating the SVG code by hand.
I've put all the code [on GitHub][github]

[github]: https://github.com/alexwlchan/art-from-spanning-trees

