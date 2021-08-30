# Linking to my work on other sites

Although I write a lot of posts on <https://alexwlchan.net>, it's not the only place I have writing.
For example, I've written articles for Last Week in AWS and the Wellcome Collection development blog.

I want a page on my personal site that links to everything I've written elsewhere, so I have a complete record of everything that I've published online.

I also want a local backup of that work.
I'm proud of it, and I don't want the only copy to be on a site that I don't control – I could lose access to it at any time.
(For more on this, see [why developers should archive their old content](https://www.stephaniemorillo.co/post/why-developers-should-archive-their-old-content) by Stephanie Morillo.)

## How I record my other work

I have a [YAML file (`elsewhere.yml`)](../src/_data/elsewhere.yml) where I create new entries for every article, talk or podcast I do:

```yaml
writing:
  - date: 2021-05-07
    title: "What is an Edge Location in AWS? A Simple Explanation"
    url: "https://www.lastweekinaws.com/blog/what-is-an-edge-location-in-aws-a-simple-explanation/"
    publication: "Last Week in AWS"
  - date: 2020-05-20
    title: "Building Wellcome Collection's new archival storage service"
    url: "https://stacks.wellcomecollection.org/building-wellcome-collections-new-archival-storage-service-3f68ff21927e"
    publication: "Wellcome Collection development blog"
```

This format is deliberately lightweight: I can add new entries quickly, as soon as something is published.
(If I can't do it quickly, it's easy for me to procrastinate or forget to add something.)

## How I display my other work

The YAML file is in the `_data` folder, which is a [special folder in Jekyll](https://jekyllrb.com/docs/datafiles/).
I can load that data in a Markdown file [which renders the entries as HTML](../src/elsewhere.md).

You can see the rendered page at <https://alexwlchan.net/elsewhere/>
