# Builds in Docker

I used Jekyll (well, [Octopress][octopress]) for the first iteration of my site, but I kept having issues with Ruby.
Half the time, I'd come to write something, and find I was unable to build the site!
Clearly sub-optimal.

Drawing inspiration [from what we do at Wellcome][platform], I've pushed the entire build process inside Docker.
When I want to build the site on a new machine, I don't need to worry about installing dependencies – it's managed entirely by Docker.

[octopress]: http://octopress.org/
[platform]: https://github.com/wellcometrust/platform
