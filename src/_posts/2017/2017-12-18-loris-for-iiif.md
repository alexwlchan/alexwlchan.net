---
layout: post
date: 2017-12-18T16:52:17.162Z
title: Using Loris for IIIF at Wellcome
summary: How we use Loris to provide a IIIF Image API for browsing our collections at Wellcome–how it runs in AWS, store our high-resolution images, and monitor the service.
tags:
  - wellcome collection
  - iiif
canonical_url: https://stacks.wellcomecollection.org/using-loris-for-iiif-at-wellcome-6ed1fefaf801
---
*I wrote this article while I was working at Wellcome Collection. It was originally published [on their Stacks blog](https://stacks.wellcomecollection.org/using-loris-for-iiif-at-wellcome-6ed1fefaf801) under a CC BY 4.0 license, and is reposted here in accordance with that license.*

<p>We’ve recently finished making over 100k images available to search on the <a href="https://wellcomecollection.org/works">new Wellcome Collection website</a>, freely available and CC-licensed.</p><p>But how do we serve these images? Many of these are high-resolution archival or medical images, meant to capture lots of detail. The image files are big—routinely thousands of pixels wide, several megabytes a piece. If you wanted to skim a book, and the book had a hundred pages, you’d download over a gigabyte of data. Ouch!</p><p>We’re serving lots of images, and we want them to be fast. We want to send small, tightly-focused files—just the data you want, and nothing else — so we provide our images through a IIIF Image Server.</p><p>In this post, I’ll explain a little of what IIIF is, and how we provide it at Wellcome.</p><h2>What is IIIF?</h2><p>IIIF is the <a href="http://iiif.io/">International Image Interoperability Framework</a>, which is a set of standards for serving large images. It’s an open standard used by many libraries and archives, and it provides a way to combine resources from different collections. When a client asks for an image, they can make a very particular request — such as size, or crop, or rotation—and the server prepares the exact image they want, and sends that along. It’s a practical way to deal with really large images.</p><p>Let’s look at a few examples of how we’re already using it.</p><p>In a page of search thumbnails, we request very small images, which load much faster than the full-sized files.</p>

<figure>
  {%
    picture
    filename="1*W-2EE9z0MG0Db_D-AwxRUA.png"
    width="750"
    alt=""
  %}
  <figcaption>A page of results if <a href="https://wellcomecollection.org/works?query=london">you search for “london”</a>.</figcaption>
</figure>

<p>On a page showing a single image, we can display a bigger image, but still not the full-sized version.</p>

<figure>
  {%
    picture
    filename="1*kaxAaXV5qTmEUs78cRQoIQ.png"
    width="750"
    alt=""
  %}
  <figcaption>An <a href="https://wellcomecollection.org/works/gu4fnd8s?query=london">individual works page</a>, showing vaccination points for smallpox. Credit: Science Museum, London. CC BY.</figcaption>
</figure>

<p>If we really want to see all the detail, we can zoom in further. Because a IIIF server allows us to request not just specific sizes, but specific crops, even this doesn’t need us to load the whole image. We can load the parts of the image we’re focusing on, and skip the rest.</p>

<figure>
  {%
    picture
    filename="1*4oR2RCD7fhpRZwZM6KShRw.png"
    width="750"
    alt=""
  %}
  <figcaption>A close-up view of <a href="https://wellcomecollection.org/works/gu4fnd8s?query=london">an individual smallpox packet</a>. Text: <em>“Liverpool Station, Dec 4th 1913, No 48 (?), 50 Points.” </em>Credit: Science Museum, London. CC BY.</figcaption>
</figure>

<p>In this example, we’ve loaded a full resolution tile for this particular card, but only that card. We’ve not downloaded the rest of the image yet, and we won’t until we move to look at a different region.</p><p>Because IIIF is a widely-used standard, there are lots of tools that can use it. For example, the zoom above is provided by <a href="https://openseadragon.github.io">OpenSeadragon</a>, a client which knows how IIIF works, and how to request specific tiles. If we’d written our own bespoke image API, we’d have to write those tools ourselves.</p><p>Wellcome was a founder and early adopter of the IIIF ecosystem.</p><h2>Picking a IIIF Image server</h2><p>We knew we wanted to use an existing (ideally open source) IIIF Image server.</p><p>Writing our own was out of the question—it would have taken months to develop and test, and at the end of it we’d be the only user. It’s much better to use an existing server that other people are already using—we know it works in production, we all share the benefits of testing and bugfixes, and we can contribute to the wider community. Image manipulation is a massive problem space, with lots of edge cases. It’s where open source really shines: together, we’re more likely to find (and fix!) all the weird corners.</p>

<figure>
  {%
    picture
    filename="SlenderLorisLyd2.png"
    width="750"
    alt=""
  %}
  <figcaption>An illustration of two Lorises. “The Slender Loris, in waking and sleeping posture.” Taken from <a href="https://commons.wikimedia.org/wiki/File:SlenderLorisLyd2.png">Royal Natural History volume 1, page 230</a>. Public domain.</figcaption>
</figure>

<p>We decided to use <a href="https://github.com/loris-imageserver/loris">Loris</a>, a IIIF Image API server available under a 2-clause BSD license. It’s a Python web application, with a lot of processing managed by libraries like Pillow, Werkzeug and cryptography. That means Loris itself is a fairly small wrapper around these libraries, focused on providing the IIIF API—it does one thing, and it does it well.</p><p>Loris provides a standard WSGI server, which we run with uWGSI. This made it really easy to get up-and-running when we first tried it, which is one of the reasons we chose it. I sat down to play with it for an afternoon, and accidentally created our first production instance!</p><h2>Architecture</h2><p>All our applications run as Docker containers inside <a href="https://aws.amazon.com/ecs/">Amazon ECS</a>, and Loris is no different.</p>

<figure>
  {%
    picture
    filename="1*R1ziR9m8j5Mi1nRKZejkhQ.png"
    width="750"
    alt=""
  %}
  <figcaption>Our architecture diagram. Requests arrive from users on the right, where they’re received by our CDN/caching layer (CloudFront). If the request isn’t cached, it’s sent to Loris running inside Docker containers on ECS, which fetch the full-sized image from S3.</figcaption>
</figure>

<p>In fact, we run two containers per Loris instance: a Python container which runs uWSGI, and an Nginx container which acts as a proxy. This is a common pattern, both for Python web applications generally, and in our platform. Nginx provides robust HTTP support and connection handling, and runs in front of Loris and our Scala applications.</p><p>Our full-sized image files, are stored in <a href="https://en.wikipedia.org/wiki/Amazon_S3">Amazon S3</a>. When Loris receives a request, it starts by fetching the full-size image from S3, before it produces the specific image that it sends to the client. Loris fetches the images over HTTP, rather than using the AWS APIs, so we could easily swap out S3 as a backend if we wanted to.</p><p>In front of Loris we have <a href="https://en.wikipedia.org/wiki/Amazon_CloudFront">Amazon CloudFront</a>. This acts as a CDN and a caching layer. If a user asks for an image that has already been requested once, it gets served from CloudFront instead of Loris—so it arrives faster, and reduces load on our containers.</p><h2>Monitoring</h2><p>We monitor Loris with CloudWatch alarms. Whenever Loris returns a 500 error, it trips an alarm, which posts a message in our Slack channel:</p>

<figure style="width: 588px;">
  {%
    picture
    filename="0*mZdf3fVx6Xk70oWC.png"
    width="588"
    alt=""
    class="screenshot"
  %}
  <figcaption>A screenshot of one of our Slack alarms. Text: “The ALB spotted a 500 error in Loris at 02:45:00 on 13 Dec 2017.” “ALB” is “Application Load Balancer”, an AWS service which routes requests to individual Docker containers.</figcaption>
</figure>

<p>This means we’re instantly notified of any problem, and we can respond quickly.</p><p>We’ve used this information to make a number of stability fixes, and because Loris is open source, we can share them with everybody. Since we started using Loris, I’ve become one of the Loris maintainers because of my patches.</p><h2>The future</h2><p>We’re very happy with our current Loris set up, and we’re not planning any immediate changes. As we expose more works on the new Wellcome Collection website, we’ll serve many more images through Loris, but this setup will probably be around for a while.</p><p>If you want to run Loris yourself, you can find our Dockerfile, Loris configuration and Terraform config in <a href="https://github.com/wellcometrust/platform/tree/master/loris">our GitHub repo</a>. You can also find Loris itself <a href="https://github.com/loris-imageserver/loris">on GitHub</a>, with all the code and installation instructions.</p><p><em>Thanks to Jonathan Tweed, Natalie Pollecutt, Robert Kenny, and Tom Scott for reviewing drafts of this post.</em></p>
