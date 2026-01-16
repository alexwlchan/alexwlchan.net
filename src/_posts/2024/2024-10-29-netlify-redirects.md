---
layout: post
date: 2024-10-29 07:17:02 +00:00
title: A script to verify my Netlify redirects
summary: |
  I wrote a script that reads my redirect rules, and checks that every redirect takes you to a page that actually exists on my site.
tags:
  - netlify
  - ruby
  - blogging about blogging
---
I've changed the URL design on this website a couple of times.
The current structure seems to be working fairly well, but I made some dubious decisions when I started out that really didn't scale.
(Like having a single folder for all of my `/images/` -- of which there are now over 1600.
I've divided it into per-year folders to make it easier to manage.)

I always create redirects when I change my URLs, so all the old URLs keep working.
This [avoids link rot][link_rot], and I think it's generally a nice thing to do.

Because the site is currently hosted on Netlify, I use their [redirect rules] to manage my redirects.
In particular, I have a plain text file [called `_redirects`][_redirects] in the publish directory of my site.
I write one redirection per line, with the old path followed by the new path.
I can write comments by starting a line with `#`, and leave empty lines to make clear gaps between different types of redirect.

Here are a few examples from my `_redirects` file:

```
# Move images into per-year folders
/images/wiki-squares.png      /images/2016/wiki-squares.png

# Fix a typo in the slug of this blog post
/2021/01/what-year-it-it/     /2021/what-year-is-it/

# Changing the name of the list of articles
/all-posts/                   /articles/
```

I wanted to make sure this file is always redirecting to valid URLs -- there's no point redirecting somebody to a broken URL!

I wrote a Ruby script that parses my `_redirects` file, and checks that every redirect rule is sending you to a URL that exists on my site.
This has already caught several typos and mistakes that I'd otherwise have missed.

[link_rot]: https://www.nngroup.com/articles/fighting-linkrot/
[redirect rules]: https://docs.netlify.com/routing/redirects/
[_redirects]: https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file
[Jekyll]: https://jekyllrb.com

## Parsing the `_redirects` file

First I needed some code that could extract my list of redirects from the `_redirects` file.
I wrote a basic parsing function:

```ruby
# Parse a Netlify `_redirects` file.
#
# The syntax of this file is described in Netlify's docs:
# https://docs.netlify.com/routing/redirects/#syntax-for-the-redirects-file
def parse_netlify_redirects(path)
  File.foreach(path).with_index(1)
      .reject { |line, _| line.start_with? '#' }
      .reject { |line, _| line.strip.empty? }
      .map do |line, lineno|
        {
          lineno:,
          source: line.strip.split[0],
          target: line.strip.split[1]
        }
      end
end
```

The `File.foreach(path).with_index(1)` gets me the lines of the file, with their line number as an index.
I'm starting at `1` so the `lineno` variables match the line numbers I see in my text editor.

The two `reject` lines are discarding comments and empty lines, respectively.

The `map` block gets the source/target of the redirect from each line.

This is only a basic parser -- the `_redirects` file has [more options](https://docs.netlify.com/routing/redirects/redirect-options/), like the ability to specify the status code of your redirect, or look for query parameters.
This code doesn't handle any of that.
But that's okay, because it only has to parse *my* `_redirects` file and extract a specific set of values.
I know I have a fairly simple file and this basic implementation is plenty.

Here's the output of this function on the example above:

```ruby
[
  {
    :lineno => 2,
    :source => "/images/wiki-squares.png",
    :target => "/images/2016/wiki-squares.png"
  }, {         
    :lineno => 5,
    :source => "/2021/01/what-year-it-it/",
    :target => "/2021/what-year-is-it/"
  }, {         
    :lineno => 8,
    :source => "/all-posts/",
    :target => "/articles/"
  }
]
```

So now we need to know: do all of those targets exist?



## Checking that my redirect targets exist

I build this site with a static site generator that writes a collection of HTML files.
These files are written to the same folder that contains the `_redirects` file, so I need to look inside that folder for the redirect targets.

This is a small example of what my site folder looks like:

```
_site
  ├─ _redirects
  ├─ articles/
  │    └─ index.html
  └─ images/
       └─ 2016/
            └─ wiki-squares.png
```

This is the code that takes the list of redirects, and checks each of them points to a file that actually exists in that folder:

```ruby
publish_dir = '_site'

# Build a list of redirects that point to a file which doesn't exist in
# my publish directory -- this means the redirect will point to a
# broken URL on the finished site.
broken_redirects =
  parse_netlify_redirects("#{publish_dir}/_redirects")
    .reject do |redirect|

      # If the target path ends in `/`, it's an HTML file.  These are
      # saved as `index.html` files inside a folder with the target path,
      # e.g. the `/articles/` page is saved at `/articles/index.html`.
      #
      # If it doesn't end in `/`, it's any other file.
      target_file =
        if redirect[:target].end_with? '/'
          "#{publish_dir}#{redirect[:target]}/index.html"
        else
          "#{publish_dir}/#{redirect[:target]}"
        end

      File.exist? target_file
    end

# If there are any broken redirects, print a list of them with their
# line numbers in the `_redirects` file for easy referencing/fixing.
if broken_redirects.empty?
  puts "Everything in `_redirects` looks good!"
else
  puts "The following line(s) in `_redirects` are broken:"

  broken_redirects.each do |redirect|
    puts "* L#{redirect[:lineno]}: #{redirect[:source]} ~> #{redirect[:target]}"
  end
end
```

If everything is fine, it just prints:

```
Everything in `_redirects` looks good!
```

If there are issues, it prints a list of lines with broken redirects:

```
The following line(s) in `_redirects` are broken:
* L5: /2021/01/what-year-it-it/ ~> /2021/what-year-is-it/
```

I run this script as part of my website build, so I can't deploy new changes if I have broken redirects.
It takes a fraction of a second to run, so most of the time I never notice it -- but whenever I'm changing my URL design or moving files around, I really appreciate the safety net.
Several times this script has saved me from breaking old links or screwing up part of the site.
