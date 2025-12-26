---
layout: post
date: 2022-09-13 18:31:40 +0000
title: Generating art from lattice graphs
summary: Randomly selecting a subset of edge from a graph can make pretty pictures.
tags:
  - generative art
  - drawing things
index:
  feature: true
---

<style type="x-text/scss">
  @use "components/checkerboard";
</style>

A couple of weeks ago, I went to see my sister playing percussion in a brass band [at the Proms][late_prom].
While I was on the train home, I had an idea for a fun art project.
I sketched it out on a napkin, got it working, posted a few pictures on Twitter, then put it down.

On Saturday I was sitting in the foyer of the Birmingham Symphony Hall, ready to watch her play in another band at [the British Open][open].
While I was waiting for her to start, I had some time to revisit those ideas, and write them up properly.

(There's a lesson here about how art begets more art.)

These are a few of the pictures I was able to make:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/brown_conlang_4.svg"
    alt="A simple graphic made of connected dark brown lines on a light brown background. All the lines are at right angles to each other, and rise up from a single horizontal line on the base. The left-hand side looks like a “y” and a “u” placed on top of each other; the right-hand side looks like a capital “E” with an extra bar."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/lime_circles.svg"
    alt="A simple graphic made of connected lime-coloured lines. They're arranged around a circle: some concentric rings around a central point, then spokes going from the centre to the outer edge. Some of the lines are missing -- some of the circles and spokes have gaps."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/purple_diamond.svg"
    alt="A simple graphic made of purple lines. They're arranged in concentric diamonds, with three of the four sides closed, but one side open."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/yellow_keyhole.svg"
    alt="A simple graphic made of thin, yellow, circular lines. There's a gap in the middle of the circle, which looks a bit like a keyhole."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/blue_circle_quadrants.svg"
    alt="A simple graphic made of connected blue lines. The circle is divided into four quadrants: in the upper-left and lower-right quadrants, the curves bend outwards; in the lower-left and upper-right quadrants, the curves bend inwards. It creates a rather pleasing visual symmetry."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/cream_clock.svg"
    alt="A simple graphic made of connected dark brown lines. The lines form a sort of curved pentagon shape, with three lines coming out of the central point that make it look vaguely like a clock."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/red_nuclear.svg"
    alt="A graphic made of connected red circular lines. They're arranged into seven segments, with three segments forming along the outer edge. This looks similar to the three sections of a radiation warning symbol."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/green_octagon.svg"
    alt="A graphic made of connected green lines, in a sort of octagonal shape."
    link_to="original"
  %}
</div>

I think these are pretty fun, and I'm surprised by how much variation I got from a single idea.
In this post, I'm going to explain my ideas and thinking, and share the code I used to make them.

[late_prom]: https://www.theguardian.com/music/2022/aug/13/bbc-proms-30-32-tredegar-band-review-hms-pinafore-opera-holland-park-ohp-poulenc-double-bill-glyndebourne
[open]: https://www.4barsrest.com/news/54320/bands-ready-for-british-open-return



## The basic idea

In maths, a [*graph*](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics)) is a structure made up of vertices and edges.
Here's a simple example:

<figure style="width: 300px; margin-top: -1em; margin-bottom: -1em;">
  {%
    inline_svg
    filename="complex_graph.svg"
    alt="A graph with various vertices (black circles) connected by grey lines."
  %}
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
  {%
    inline_svg
    filename="graph-art/grey_conlang_1.svg"
    alt="A graphic made of straight grey lines arranged at right angles to each other. It looks a bit like a U, a T and an H smushed together."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_conlang_2.svg"
    alt="A graphic made of straight grey lines arranged at right angles to each other. There's a big enclosing square and then a slightly smaller square in the upper-left, a bit like one is enclosing the other."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_conlang_3.svg"
    alt="A graphic made of straight grey lines arranged at right angles to each other. There's a small square in the lower left-hand corner, with a few lines coming off it – a bit like tentacles or hairs."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_conlang_4.svg"
    alt="A graphic made of straight grey lines arranged at right angles to each other. To my eye, this looks a bit like two representations of people walking from left-to-right."
    link_to="original"
  %}
</div>

When I shared them on Twitter, somebody compared them to the characters of a [conlang ("constructed language")][conlang].
I quite liked the comparison, so I drew another batch with an earthy brown and varying stroke widths:

<div class="grid_4up">
  {%
    inline_svg
    filename="graph-art/brown_conlang_1.svg"
    alt="A graphic made of connected dark brown lines on a light brown background. The lines are quite thin, and appear to be creating a shape in an approximation of a clockwise spiral."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/brown_conlang_2.svg"
    alt="A graphic made of connected dark brown lines on a light brown background. The lines are very thick."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/brown_conlang_3.svg"
    alt="A graphic made of connected dark brown lines on a light brown background. There's a distinct 'left' and 'right' half to the graphic, both forming distinct shapes on either side."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/brown_conlang_4.svg"
    alt="A simple graphic made of connected dark brown lines on a light brown background. All the lines are at right angles to each other, and rise up from a single horizontal line on the base. The left-hand side looks like a “y” and a “u” placed on top of each other; the right-hand side looks like a capital “E” with an extra bar."
    link_to="original"
  %}
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
  {%
    inline_svg
    filename="graph-art/vines.0.svg"
    alt="A simple graphic made of dark green lines on a light green background. The lines are arranged at right angles or 45 degrees to each other, and look a bit like a vine hanging down a long wall."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/vines.1.svg"
    alt="A simple graphic made of dark green lines on a light green background. The lines are arranged at right angles or 45 degrees to each other, and look a bit like a vine hanging down a long wall."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/vines.2.svg"
    alt="A simple graphic made of dark green lines on a light green background. The lines are arranged at right angles or 45 degrees to each other, and look a bit like a vine hanging down a long wall."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/vines.3.svg"
    alt="A simple graphic made of dark green lines on a light green background. The lines are arranged at right angles or 45 degrees to each other, and look a bit like a vine hanging down a long wall."
  %}
</div>



## Input graph #3: radial lattice

I wanted to try using spiderweb-like diagrams as the input; I thought they'd look fun:

<div class="grid_4up">
  {%
    inline_svg
    filename="graph-art/radial-3.svg"
    alt="Three concentric grey rings, with three spokes going from the centre to the outermost ring."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/radial-5.svg"
    alt="Three concentric grey rings, with five spokes going from the centre to the outermost ring."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/radial-8.svg"
    alt="Three concentric grey rings, with eight spokes going from the centre to the outermost ring."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/radial-20.svg"
    alt="Three concentric grey rings, with twenty spokes going from the centre to the outermost ring."
    link_to="original"
  %}
</div>

Although I wanted to use circles, drawing the curved arcs proved to be a bit tricky, so I started with straight lines between spokes.
I fixed the number of rings at 4, and just varied the number of spokes.
I also experimented with removing the central point, which creates a sort of "open" core.

It took a bit of time to work out the bugs, but I really like the results:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/grey_lattice_1.svg"
    alt="A partially completed octagonal lattice made of thin grey lines."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_2.svg"
    alt="A partially completed pentagonal lattice made of thin grey lines. The central point and two sides are missing, making it feel quite open."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_4.svg"
    alt="A partially completed decagonal lattice (ten sides) made of thin grey lines. Several of the segments are completely empty; others are filled."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_3.svg"
    alt="A partially completed hexagonal lattice made of thin grey lines. Three of the lines in the upper left look a bit like the edge of a wing, as if it's flying."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_5.svg"
    alt="A partially completed octagonal lattice. Most of the lines are spokes, not the concentric octagons."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_6.svg"
    alt="A partially completed radial lattice (don't ask me to count the number of sides). Although all the edges are straight lines, it looks a bit like a circle."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_7.svg"
    alt="A partially completed pentagonal lattice made of thin grey lines. Unlike the previous lattice, the central point is included, and the three lines going into the centre give it quite a different look."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/grey_lattice_8.svg"
    alt="A partially completed radial lattice (don't ask me to count the number of sides). Although all the edges are straight lines, it looks a bit like a circle."
    link_to="original"
  %}
</div>

Then I added even more randomness: varying the number of rings, the colour, and the stroke width.
These are a few of my favourites:

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/purple_diamond.svg"
    alt="A simple graphic made of purple lines. They're arranged in concentric diamonds, with three of the four sides closed, but one side open."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/pink_pentagon.svg"
    alt="A graphic made of pink lines on a dark background. They're arranged in a pentagonal shape, with two of the five sides mostly open."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/light_heptagon.svg"
    alt="A graphic made of dark lines on a cream background. They're arranged in a heptagon shape, with several spokes almost completely open, giving a sense of direction: as if the shape is moving up the page."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/blue_hexagon.svg"
    alt="A graphic made of blue lines in a hexagon shape. There's a spoke running through the centre, and the two upper-right sides are open, helping to give a very clear sense of direction: this shape is moving up and to the right."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/ghost_heptagon.svg"
    alt="A simple graphic made of connected light blue lines. Set against the dark background, it has a vaguely ghostly effect."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/orange_many_gon.svg"
    alt="A graphic made of many orange lines. Although every line is straight, there's enough of them that the overall pattern looks a bit like a circle."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/minimal_triangle.svg"
    alt="A simple graphic made up of just of five lines, and which still makes the outline of the original triangle clear (even though only one side is drawn)."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/green_octagon.svg"
    alt="A graphic made of connected green lines, in a sort of octagonal shape."
    link_to="original"
  %}
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
  {%
    inline_svg
    filename="graph-art/experimental.svg"
    alt="A collection of grey circular arcs, where the area between the curve and the straight line connecting two points has been filled in black."
    class="nohover"
    link_to="original"
  %}
</figure>

Once I had the code for curves working, adding it to the radial lattice was fairly straightforward.
I had a lot of fun generating these images.

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/yellow_busy.svg"
    alt="A graphic made of yellow lines and circular arcs. There are lots of spokes and little arcs, so it looks quite busy."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/red_nuclear.svg"
    alt="A graphic made of connected red circular lines. They're arranged into seven segments, with three segments forming along the outer edge. This looks similar to the three sections of a radiation warning symbol."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/green_radar.svg"
    alt="A graphic made of dark green lines and circular arcs. To me, it looks a bit like some sort of complex radar scanning screen."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/lime_circles.svg"
    alt="A simple graphic made of connected lime-coloured lines. They're arranged around a circle: some concentric rings around a central point, then spokes going from the centre to the outer edge. Some of the lines are missing -- some of the circles and spokes have gaps."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/yellow_keyhole.svg"
    alt="A simple graphic made of thin, yellow, circular lines. There's a gap in the middle of the circle, which looks a bit like a keyhole."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/pink_half_circle.svg"
    alt="A graphic made of pink lines and quarter circle arcs. The arrangement of lines and arcs around the central vertical line look a bit like a helmet, or maybe a stylised face."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/orange_circle.svg"
    alt="A graphic made of thick orange lines and circular arcs."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/lavendar_pentagram.svg"
    alt="A graphic made of black lines and circular arcs. There are five spokes which makes it look vaguely like a star."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/tri_circle.svg"
    alt="A graphic made of thick blue lines and circular arcs, split into three segments. It looks vaguely like some sort of radar scanner."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/turquoise_busy.svg"
    alt="A graphic made of turquoise lines and circular arcs. There are lots of spokes and little arcs, so it looks quite busy."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/purple_semicircle.svg"
    alt="A graphic made of purple semicircular arcs. You can see where the complete circle should be, but the graphic is divided down the middle: there are only arcs on the left-hand side."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/blue_quarters.svg"
    alt="A graphic made of thick blue lines and circular arcs, split into quarters. It looks vaguely like some sort of radar scanner."
    link_to="original"
  %}
</div>

These feel like designs out of science-fiction: the red circles feels evocative of radiation warnings, and several of them look like radar scanning screens (especially the dark green).
As the spoke count increases, some of them feel like large mazes.
The thin yellow line is one of my favourites, because it reminds me of a key hole.

Once again, I think some of the most striking images are those with just a few spokes and rings.

[curved_arcs]: /2022/circle-party/



## Input graph #5: radial lattice with convave curves

For a final variation, I tried using concave curves in the lattice.
This matches the spider-web emoji, where the individual arcs bend towards the centre of the circle, rather than outward.

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/four_point_curve.svg"
    alt="A graphic made of pink curves around a four pointed cross. The four points are at right angles; three of the right angles have sweeping curves that approach the centre, but the fourth is empty."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/spider_hex.svg"
    alt="A blue graphic that looks a bit like a six-pointed spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/purple_spider.svg"
    alt="A purple graphic that looks a bit like a large, lavender spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/octo_spider.svg"
    alt="A green graphic that looks a bit like an eight-pointed spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/orange_spider.svg"
    alt="An orange graphic that looks a bit like a five-pointed spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/silver_spider.svg"
    alt="A black-and-white graphic that looks like a damaged spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/green_spider.svg"
    alt="A green graphic that looks like a damaged spider web."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/ochre_spider.svg"
    alt="An ochre graphic that looks like a damaged seven-point spider web."
    link_to="original"
  %}
</div>

This got even more fun when I allowed arcs to bend alternately in and out, creating some extremely funky patterns.

<div class="grid_4up checkerboard">
  {%
    inline_svg
    filename="graph-art/swirly.svg"
    alt="A purple graphic with curves moving in and out along the spokes."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/inverse_three_points.svg"
    alt="A lime graphic with three curves making a triangle. Two of the curves are concave and intersecting, so it looks a bit like an upwards arrow."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/blue_circle_quadrants.svg"
    alt="A simple graphic made of connected blue lines. The circle is divided into four quadrants: in the upper-left and lower-right quadrants, the curves bend outwards; in the lower-left and upper-right quadrants, the curves bend inwards. It creates a rather pleasing visual symmetry."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/curvy_hexagon.svg"
    alt="An orange graphic with three sets of curves bending inwards, three outwards, to form a sort of curvy hexagon."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/cream_clock.svg"
    alt="A simple graphic made of connected dark brown lines. The lines form a sort of curved pentagon shape, with three lines coming out of the central point that make it look vaguely like a clock."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/orange_starburst.svg"
    alt="An orange graphic with four sets of curves bending inwards, four outwards, to form a sort of curvy octagon."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/purple_splodge.svg"
    alt="A purple graphic that looks a bit like an octagon with a bunch of sides removed."
    link_to="original"
  %}
  {%
    inline_svg
    filename="graph-art/red_heptagon.svg"
    alt="A red graphic that looks a bit like a curvy heptagon. Two of the segments have a lot of filled in lines, so it looks vaguely as if it's moving upwards."
    link_to="original"
  %}
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
