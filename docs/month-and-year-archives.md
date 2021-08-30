# Month and year archives

The format of my post URLs is:

```
/:year/:month/:title/
```

Because I'm old-fashioned and think URLs are meaningful, it feels to me that `/:year/:month/` should show you a collection of all the posts in that month, and `/:year/` should do the same for the year.
The path can be treated as a directory structure – which it is, if you look at the generated files!

To that end, I'm using [another plugin](../src/_plugins/archive_generator.rb) to generate them just the way I like.
It's a fork of [jekyll-monthly-archive-plugin][archive], but with my own template and support for yearly archives as well.

[archive]: https://github.com/shigeya/jekyll-monthly-archive-plugin
