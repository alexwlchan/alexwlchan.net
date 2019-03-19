---
layout: post
date: 2019-02-26 20:27:45 +0000
category: Blogging about blogging
title: "Checking Jekyll sites with HTMLProofer"
summary:
tags:
- jekyll
---

Here's a quick change I've just made to my Jekyll setup: I've added HTML linting with [HTMLProofer][html_proofer].

HTMLProofer is a Ruby library that can validate HTML files -- checking that links and internal references work, images have alt tags, HTML markup is valid, and so on.
I was already doing a few of those checks with some hand-rolled scripts, but passing it off to a library is much nicer.
I have less code to maintain, and I get more thorough error checking to boot.

Adding it to my setup was pleasantly easy.
I added one line to my `Gemfile`:

```ruby
gem "html-proofer", "~> 3.2"
```

and then I added a small plugin to my `_plugins` directory:

```ruby
require "html-proofer"

Jekyll::Hooks.register :site, :post_write do |site|
  HTMLProofer.check_directory(site.config["destination"], opts = {
    :check_html => true,
    :check_img_http => true,
    :disable_external => true,
    :report_invalid_tags => true,
  }).run
end
```

This creates a [Jekyll hook][hooks] that runs after the entire site has been written to disk.
It calls the HTMLProofer library, looking at all the HTML files that Jekyll has just created.
If it finds any errors, it throws an exception and the build fails.

When I first ran with HTMLProofer enabled, it found nearly a thousand errors -- mostly missing alt text on images.
For now it's not running on every build, but I'm planning to fix up the errors and then turn on these checks everywhere.
That way, I'll know immediately if I've done something wrong.

This sort of library is why I really like using Jekyll, rather than maintaining my own static site generator.
There's a rich ecosystem of plugins and tools that I can use straight away, rather than building from scratch.
It was really easy to put this together -- less than ten minutes from start to finish.
That means less time programming, and more time for writing.

[html_proofer]: https://github.com/gjtorikian/html-proofer
[hooks]: https://jekyllrb.com/docs/plugins/hooks/
