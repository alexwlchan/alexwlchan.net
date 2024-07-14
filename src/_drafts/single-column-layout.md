---
layout: post
title: single-column-layout
summary:
tags:
colors:
  css_light: "#0b53ad"
  css_dark:  "#d9d9d6"
---
have a single-column layout I use for all my web pages

{%
  picture
  filename="one_column.png"
  width="400"
%}

header at top of page; footer at bottom
usually some solid colour or texture to separate from main content of the page
want to be centred at a readable width -- don't make too wide

how to do this in CSS?

I have CSS snippets I've been copying from project to project
wanted to sit down and make it work properly

basic HTML skeleton
let's apply some CSS to make it look pretty

## pushign header all the way to the top

header at top of page by default
add coloured background
but has white border around page

## pushign footer allt he way to the bottom

add coloured background
want at bottom of screen, even if main text is a bit short
let's do flex!

## centering all the text

max-width, auto
why auto?

## final snippet

I have this snippet bound to !html
as well as default css, includes some basic `<script>` and `<link>` tags because I can never remember how to use them without an example