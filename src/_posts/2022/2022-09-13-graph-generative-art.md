---
layout: post
date: 2022-09-13 18:31:40 +0000
title: Generating art from lattice graphs
summary: Randomly selecting a subset of edge from a graph can make pretty pictures.
tags: generative-art drawing-things
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

  .grid_4up a:hover {
    background: none;
  }

  .grid_4up svg {
    max-width: 100%;
  }

  @media screen and (max-width: 500px) {
    .grid_4up {
      grid-template-columns: auto auto;
    }
  }

  @media screen and (max-width: 500px) {
    .checkerboard {
      grid-auto-flow: dense;
    }

    .checkerboard svg:nth-child(8n+3),
    .checkerboard a:nth-child(8n+3),
    .checkerboard svg:nth-child(8n+5),
    .checkerboard a:nth-child(8n+5),
    .checkerboard svg:nth-child(8n),
    .checkerboard a:nth-child(8n) {
      grid-column: 2 / 2;
    }

    .checkerboard svg:nth-child(8n+6),
    .checkerboard a:nth-child(8n+6),
    .checkerboard svg:nth-child(8n+7),
    .checkerboard a:nth-child(8n+7) {
      grid-column: 1 / 2;
    }
  }
</style>

A couple of weeks ago, I went to see my sister playing percussion in a brass band [at the Proms][late_prom].
While I was on the train home, I had an idea for a fun art project.
I sketched it out on a napkin, got it working, posted a few pictures on Twitter, then put it down.

On Saturday I was sitting in the foyer of the Birmingham Symphony Hall, ready to watch her play in another band at [the British Open][open].
While I was waiting for her to start, I had some time to revisit those ideas, and write them up properly.

(There's a lesson here about how art begets more art.)

These are a few of the pictures I was able to make:

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/brown_conlang_4.svg">
    {% inline_svg "_images/2022/graph-art/brown_conlang_4.svg" %}
  </a>
  <a href="/images/2022/graph-art/lime_circles.svg">
    {% inline_svg "_images/2022/graph-art/lime_circles.svg" %}
  </a>
  <a href="/images/2022/graph-art/purple_diamond.svg">
    {% inline_svg "_images/2022/graph-art/purple_diamond.svg" %}
  </a>
  <a href="/images/2022/graph-art/yellow_keyhole.svg">
    {% inline_svg "_images/2022/graph-art/yellow_keyhole.svg" %}
  </a>
  <a href="/images/2022/graph-art/blue_circle_quadrants.svg">
    {% inline_svg "_images/2022/graph-art/blue_circle_quadrants.svg" %}
  </a>
  <a href="/images/2022/graph-art/cream_clock.svg">
    {% inline_svg "_images/2022/graph-art/cream_clock.svg" %}
  </a>
  <a href="/images/2022/graph-art/red_nuclear.svg">
    {% inline_svg "_images/2022/graph-art/red_nuclear.svg" %}
  </a>
  <a href="/images/2022/graph-art/green_octagon.svg">
    {% inline_svg "_images/2022/graph-art/green_octagon.svg" %}
  </a>
</div>

I think these are pretty fun, and I'm surprised by how much variation I got from a single idea.
In this post, I'm going to explain my ideas and thinking, and share the code I used to make them.

[late_prom]: https://www.theguardian.com/music/2022/aug/13/bbc-proms-30-32-tredegar-band-review-hms-pinafore-opera-holland-park-ohp-poulenc-double-bill-glyndebourne
[open]: https://www.4barsrest.com/news/54320/bands-ready-for-british-open-return



## The basic idea

In maths, a [*graph*](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) is a structure made up of vertices and edges.
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
By deleting edges at random (but keeping the graph connected), these are some of the pictures I was able to make:

<div class="grid_4up">
  <a href="/images/2022/graph-art/grey_conlang_1.svg">
    {% inline_svg "_images/2022/graph-art/grey_conlang_1.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_conlang_2.svg">
    {% inline_svg "_images/2022/graph-art/grey_conlang_2.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_conlang_3.svg">
    {% inline_svg "_images/2022/graph-art/grey_conlang_3.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_conlang_4.svg">
    {% inline_svg "_images/2022/graph-art/grey_conlang_4.svg" %}
  </a>
</div>

When I shared them on Twitter, somebody compared them to the characters of a [conlang ("constructed language")][conlang].
I quite liked the comparison, so I drew another batch with an earthy brown and varying stroke widths:

<div class="grid_4up">
  <a href="/images/2022/graph-art/brown_conlang_1.svg">
    {% inline_svg "_images/2022/graph-art/brown_conlang_1.svg" %}
  </a>
  <a href="/images/2022/graph-art/brown_conlang_2.svg">
    {% inline_svg "_images/2022/graph-art/brown_conlang_2.svg" %}
  </a>
  <a href="/images/2022/graph-art/brown_conlang_3.svg">
    {% inline_svg "_images/2022/graph-art/brown_conlang_3.svg" %}
  </a>
  <a href="/images/2022/graph-art/brown_conlang_4.svg">
    {% inline_svg "_images/2022/graph-art/brown_conlang_4.svg" %}
  </a>
</div>

To me, these images feel vaguely evocative of Chinese characters, or kanji.

[conlang]: https://en.wikipedia.org/wiki/Constructed_language
[square lattice]: https://en.wikipedia.org/wiki/Square_lattice



## Input graph #2: triangular lattice

When I was drawing the square lattices, I used a networkx function called `grid_2d_graph`.
While reading the documentation, I discovered another function called [`triangular_lattice_graph`][tri_lattice].
I had no idea a triangular lattice graph was, but it dropped straight into my code, so I tried it.

That gave me a set of patterns that felt like creeping vines on a wall, so I coloured them green:

[tri_lattice]: https://networkx.org/documentation/stable/reference/generated/networkx.generators.lattice.triangular_lattice_graph.html?highlight=triangular+lattice#networkx.generators.lattice.triangular_lattice_graph

<div class="grid_4up">
  <a href="/images/2022/graph-art/vines.0.svg">
    {% inline_svg "_images/2022/graph-art/vines.0.svg" %}
  </a>
  <a href="/images/2022/graph-art/vines.1.svg">
    {% inline_svg "_images/2022/graph-art/vines.1.svg" %}
  </a>
  <a href="/images/2022/graph-art/vines.2.svg">
    {% inline_svg "_images/2022/graph-art/vines.2.svg" %}
  </a>
  <a href="/images/2022/graph-art/vines.3.svg">
    {% inline_svg "_images/2022/graph-art/vines.3.svg" %}
  </a>
</div>



## Input graph #3: radial lattice

I wanted to try using spiderweb-like diagrams as the input; I thought they'd look fun:

<div class="grid_4up">
  <a href="/images/2022/graph-art/radial-3.svg">
    {% inline_svg "_images/2022/graph-art/radial-3.svg" %}
  </a>
  <a href="/images/2022/graph-art/radial-5.svg">
    {% inline_svg "_images/2022/graph-art/radial-5.svg" %}
  </a>
  <a href="/images/2022/graph-art/radial-8.svg">
    {% inline_svg "_images/2022/graph-art/radial-8.svg" %}
  </a>
  <a href="/images/2022/graph-art/radial-20.svg">
    {% inline_svg "_images/2022/graph-art/radial-20.svg" %}
  </a>
</div>

Although I wanted to use circles, drawing the curved arcs proved to be a bit tricky, so I started with straight lines between spokes.
I fixed the number of rings at 4, and just varied the number of spokes.
I also experimented with removing the central point, which creates a sort of "open" core.

It took a bit of time to work out the bugs, but I really like the results:

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/grey_lattice_1.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_1.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_2.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_2.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_4.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_4.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_3.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_3.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_5.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_5.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_6.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_6.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_7.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_7.svg" %}
  </a>
  <a href="/images/2022/graph-art/grey_lattice_8.svg">
    {% inline_svg "_images/2022/graph-art/grey_lattice_8.svg" %}
  </a>
</div>

Then I added even more randomness: varying the number of rings, the colour, and the stroke width.
These are a few of my favourites:

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/purple_diamond.svg">
    {% inline_svg "_images/2022/graph-art/purple_diamond.svg" %}
  </a>
  <a href="/images/2022/graph-art/pink_pentagon.svg">
    {% inline_svg "_images/2022/graph-art/pink_pentagon.svg" %}
  </a>
  <a href="/images/2022/graph-art/light_heptagon.svg">
    {% inline_svg "_images/2022/graph-art/light_heptagon.svg" %}
  </a>
  <a href="/images/2022/graph-art/blue_hexagon.svg">
    {% inline_svg "_images/2022/graph-art/blue_hexagon.svg" %}
  </a>
  <a href="/images/2022/graph-art/ghost_heptagon.svg">
    {% inline_svg "_images/2022/graph-art/ghost_heptagon.svg" %}
  </a>
  <a href="/images/2022/graph-art/orange_many_gon.svg">
    {% inline_svg "_images/2022/graph-art/orange_many_gon.svg" %}
  </a>
  <a href="/images/2022/graph-art/minimal_triangle.svg">
    {% inline_svg "_images/2022/graph-art/minimal_triangle.svg" %}
  </a>
  <a href="/images/2022/graph-art/green_octagon.svg">
    {% inline_svg "_images/2022/graph-art/green_octagon.svg" %}
  </a>
</div>

I especially like the blue hexagon, which feels like the topdown view of some sort of seafaring vessel.

On reflection, I can already see that "less is more".
Some of the most striking images are those with just a few spokes, or just a few rings -- as those numbers increase, the shapes get more crowded and noisy.
You're less likely to get an interesting pattern.



## Input graph #4: radial lattice with curves

As you crank up the number of spokes in a radial lattice, it starts to approximate a circle -- so I wondered if I could actually do proper curves in the lattice?
This requires the ability to draw arbitrary curved arcs, which took a bit more work, and ended up [as a separate post][curved_arcs].

Honourable mention to these image, which was created when I didn't set a `fill` attribute properly.
I didn't take this any further, but the opportunity for slices of a second colour feels like an interesting idea to explore.

<style>
  a.nohover:hover {
    background: none;
  }
</style>

<figure style="max-width: 157px;">
  <a href="/images/2022/graph-art/experimental.svg" class="nohover">
    {% inline_svg "_images/2022/graph-art/experimental.svg" %}
  </a>
</figure>

Once I had the code for curves working, adding it to the radial lattice was fairly straightforward.
I had a lot of fun generating these images.

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/yellow_busy.svg">
    {% inline_svg "_images/2022/graph-art/yellow_busy.svg" %}
  </a>
  <a href="/images/2022/graph-art/red_nuclear.svg">
    {% inline_svg "_images/2022/graph-art/red_nuclear.svg" %}
  </a>
  <a href="/images/2022/graph-art/green_radar.svg">
    {% inline_svg "_images/2022/graph-art/green_radar.svg" %}
  </a>
  <a href="/images/2022/graph-art/lime_circles.svg">
    {% inline_svg "_images/2022/graph-art/lime_circles.svg" %}
  </a>
  <a href="/images/2022/graph-art/yellow_keyhole.svg">
    {% inline_svg "_images/2022/graph-art/yellow_keyhole.svg" %}
  </a>
  <a href="/images/2022/graph-art/pink_half_circle.svg">
    {% inline_svg "_images/2022/graph-art/pink_half_circle.svg" %}
  </a>
  <a href="/images/2022/graph-art/orange_circle.svg">
    {% inline_svg "_images/2022/graph-art/orange_circle.svg" %}
  </a>
  <a href="/images/2022/graph-art/lavendar_pentagram.svg">
    {% inline_svg "_images/2022/graph-art/lavendar_pentagram.svg" %}
  </a>
  <a href="/images/2022/graph-art/tri_circle.svg">
    {% inline_svg "_images/2022/graph-art/tri_circle.svg" %}
  </a>
  <a href="/images/2022/graph-art/turquoise_busy.svg">
    {% inline_svg "_images/2022/graph-art/turquoise_busy.svg" %}
  </a>
  <a href="/images/2022/graph-art/purple_semicircle.svg">
    {% inline_svg "_images/2022/graph-art/purple_semicircle.svg" %}
  </a>
  <a href="/images/2022/graph-art/blue_quarters.svg">
    {% inline_svg "_images/2022/graph-art/blue_quarters.svg" %}
  </a>
</div>

These feel like designs out of science-fiction: the red circles feels evocative of radiation warnings, and several of them look like radar scanning screens (especially the dark green).
As the spoke count increases, some of them feel like large mazes.
The thin yellow line is one of my favourites, because it reminds me of a key hole.

Once again, I think some of the most striking images are those with just a few spokes and rings.

[curved_arcs]: {% post_url 2022/2022-08-10-circle-party %}



## Input graph #5: radial lattice with convave curves

For a final variation, I tried using concave curves in the lattice.
This matches the spider-web emoji, where the individual arcs bend towards the centre of the circle, rather than outward.

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/four_point_curve.svg">
    {% inline_svg "_images/2022/graph-art/four_point_curve.svg" %}
  </a>
  <a href="/images/2022/graph-art/spider_hex.svg">
    {% inline_svg "_images/2022/graph-art/spider_hex.svg" %}
  </a>
  <a href="/images/2022/graph-art/purple_spider.svg">
    {% inline_svg "_images/2022/graph-art/purple_spider.svg" %}
  </a>
  <a href="/images/2022/graph-art/octo_spider.svg">
    {% inline_svg "_images/2022/graph-art/octo_spider.svg" %}
  </a>
  <a href="/images/2022/graph-art/orange_spider.svg">
    {% inline_svg "_images/2022/graph-art/orange_spider.svg" %}
  </a>
  <a href="/images/2022/graph-art/silver_spider.svg">
    {% inline_svg "_images/2022/graph-art/silver_spider.svg" %}
  </a>
  <a href="/images/2022/graph-art/green_spider.svg">
    {% inline_svg "_images/2022/graph-art/green_spider.svg" %}
  </a>
  <a href="/images/2022/graph-art/ochre_spider.svg">
    {% inline_svg "_images/2022/graph-art/ochre_spider.svg" %}
  </a>
</div>

This got even more fun when I allowed arcs to bend alternately in and out, creating some extremely funky patterns.

<div class="grid_4up checkerboard">
  <a href="/images/2022/graph-art/swirly.svg">
    {% inline_svg "_images/2022/graph-art/swirly.svg" %}
  </a>
  <a href="/images/2022/graph-art/inverse_three_points.svg">
    {% inline_svg "_images/2022/graph-art/inverse_three_points.svg" %}
  </a>
  <a href="/images/2022/graph-art/blue_circle_quadrants.svg">
    {% inline_svg "_images/2022/graph-art/blue_circle_quadrants.svg" %}
  </a>
  <a href="/images/2022/graph-art/curvy_hexagon.svg">
    {% inline_svg "_images/2022/graph-art/curvy_hexagon.svg" %}
  </a>
  <a href="/images/2022/graph-art/cream_clock.svg">
    {% inline_svg "_images/2022/graph-art/cream_clock.svg" %}
  </a>
  <a href="/images/2022/graph-art/orange_starburst.svg">
    {% inline_svg "_images/2022/graph-art/orange_starburst.svg" %}
  </a>
  <a href="/images/2022/graph-art/purple_splodge.svg">
    {% inline_svg "_images/2022/graph-art/purple_splodge.svg" %}
  </a>
  <a href="/images/2022/graph-art/red_heptagon.svg">
    {% inline_svg "_images/2022/graph-art/red_heptagon.svg" %}
  </a>
</div>

At one point I had this running in a background window, generating a new image every thirty seconds, which made for a fun bit of decoration.



## Further ideas

The only limit here is the graphs you start with: the stranger the input, the stranger the output.
I have a bunch of ideas for other variations I could try, including:

* rotating the initial graph
* allowing for non-uniform gaps between spokes/rings in the radial lattice
* adding markers to the leaf nodes
* systematically deleting chunks of the original graph, say alternate spokes
* create filled segments, not just lines

I have no immediate plans to work on this any further -- I proved the initial idea is workable, and I got some pretty pictures.
That's enough for now.

I mentioned earlier that some of the patterns look like the walls of a maze.
These wouldn't actually work as mazes, but it feels like this isn't too far from a maze generator.
Maybe if you used this to create the negative space, not the walls?

I made these with some scrappy Python scripts, using [networkx] for the graph logic and generating the SVG markup with string templates.
I've put the code [on GitHub][github], although it's not documented.

There's no point or greater moral to this post; I just made some pictures that I think are pretty and interesting.
They don't serve a purpose, and that's okay.
I spend a lot of time doing work on the computer, and it's nice to use it for fun things too.

[github]: https://github.com/alexwlchan/art-from-spanning-trees
