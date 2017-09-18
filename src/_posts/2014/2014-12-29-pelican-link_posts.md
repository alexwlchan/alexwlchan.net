---
date: 2014-12-29 08:26:00 +0000
layout: post
slug: pelican-linkposts
tags: pelican python
title: RSS linkposts in Pelican
---

You may have noticed that linkposts have started appearing on the blog. This is, of course, [not an original idea][df].

I use [Pelican][pelican] to generate the site, so I needed to find a linked list implementation that worked in Pelican. I started with [Gabe Weatherhead's post][gabe] which explained how to add a `link` attribute to my Markdown source files, and I modified my templates and CSS for the linkposts. But Gabe's post ended on a loose thread, which I felt compelled to pull on:

> I'm still trying to understand how to create RSS feed link-style articles.

In most RSS feeds with linked lists, the main URL points to the original source, not the commentary on the host site. That's what I wanted to implement in Pelican. (I don't know if Gabe ever found the answer, but if he did, I can't find where he wrote about it. I was also unable to find anybody else who'd done this before.)

<!-- summary -->

I couldn't find anything in the configuration, or the templates, for creating this sort of feed item, so I decided to find the code which generates the XML that goes into the RSS feed. I tracked it to a file in the Pelican module: `writers.py`. On my machine, the full path was

```
~/.virtualenvs/pelican/lib/python2.7/site-packages/pelican/writers.py
```

This module contains a function, `_add_item_to_the_feed`, which gets the attributes for a post, then passes it to the `add_item` method on the `feed` object. One of the arguments passed to `add_item` is the main URL of the post. By intercepting this and replacing its value with the `link` from the Markdown headers, we can redirect the RSS feed to the linked post. I'm also appending an arrow to the title of the post, and a permalink to the post body.

This is the diff:

```diff
diff --git a/writers.py b/writers.py
index 61acdad..d899f99 100644
--- a/writers.py
+++ b/writers.py
@@ -41,16 +41,22 @@ class Writer(object):
         return feed

     def _add_item_to_the_feed(self, feed, item):

-        title = Markup(item.title).striptags()
-        link = '%s/%s' % (self.site_url, item.url)
+        article_link = '%s/%s' % (self.site_url, item.url)
+        if hasattr(item, 'link'):
+            title = Markup(item.title + " →").striptags()
+            link = item.link
+            description=item.get_content(self.site_url) + "<p><a href=\"%s\">Permalink ∞</a></p>" % article_link
+        else:
+            title = Markup(item.title).striptags()
+            link = article_link
+            description=item.get_content(self.site_url)
+
         feed.add_item(
             title=title,
             link=link,
             unique_id='tag:%s,%s:%s' % (urlparse(link).netloc,
                                         item.date.date(),
                                         urlparse(link).path.lstrip('/')),
-            description=item.get_content(self.site_url),
+            description=description,
             categories=item.tags if hasattr(item, 'tags') else None,
             author_name=getattr(item, 'author', ''),
             pubdate=set_date_tzinfo(
```

I'm not keen on patching my Pelican installation like this, because it's a bit fragile and I'll have to reapply the patch if I ever reinstall. I've made an exception for this change, because it's fairly critical to how link posts work, but I don't expect to make many more changes like this.

[df]: http://daringfireball.net/linked/
[pelican]: http://getpelican.com/
[gabe]: http://www.macdrifter.com/2012/08/linked-list-posts-in-pelican.html
