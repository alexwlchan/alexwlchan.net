---
layout: post
title: netlify-bandwidth-graph
summary:
tags:
  - netlify
  - drawing-things
---
I currnetly host thsi site on Netlify
Free Plan, so I get 100GB of bandwidth a month

I can see how much bandwidth I have in the Netlify console, but 2 problems:

1. I never log into the console, only use the CLI + GitHub Actions
2. No sense of proportion - 50% is bad on day 1, fine on day N-1

So used the Netlify API to build my own graph.
Here's what it looks like:

[insert]

## getting the data

netlify exposes the data through an api
need (1) your team slug and (2) api key
(kinda annoying that api kesy have no scope)

[example request / output]

explain output in terms of gibibytes, dates

## being a good api citizen

use the etag header

## drawing this as a pie chart

i prefer pie charts for proprtions -- easier to judge halfway, quarters etc compared to a bar
want to see if bandwidth use is keeping track with pace
idea: two part pie chart

let's draw it as an svg: javascript
