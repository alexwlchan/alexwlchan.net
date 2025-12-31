---
layout: post
date: 2014-08-31 12:12:00 +0000
tags:
  - tumblr
title: Updates to my site for finding untagged Tumblr posts
---

About two weeks ago, I took a family holiday to Oslo. When I came back, I found that my site for [finding untagged Tumblr posts][post1] had received a lot of traffic while I was gone. I'm flattered that so many people have found it useful.

This heavy usage also exposed several bugs in the original design. The site would become unresponsive if there were lots of untagged posts (sometimes in the tens of thousands). I've pushed out an update to fix this: you can click **"Do you have lots of posts?"** to limit the number of posts that get shown. This should fix any bugs with browsers freezing up.

If you have any other problems or suggestions, then please <a href="mailto:alex@alexwlchan.net?subject=Feedback on 'Find Untagged Tumblr Posts' site">get in touch</a>.

The rest of this post explains the major changes.

## Don't start multiple HTTP requests simultaneously

The Tumblr API returns up to 20&nbsp;posts at a time, so to get all the posts from a blog, you need to make `(total number of posts)/20` requests.

In the first version of the site, I didn't think to queue these requests, so the site would start making requests as fast as it could. I didn't consider what this might to do a browser tab or the Tumblr API. Oops.

This is very irresponsible use of the Tumblr API, and I'm disappointed that I didn't realise this before.

The site has been modified so that each batch of 20&nbsp;posts is loaded one-at-a-time, only after the previous batch has loaded successfully. This should alleviate the load on both browsers and Tumblr's servers.

## Filter in the controller, not on the page

The Tumblr API returns a single blog post as a JSON object. This object includes all of the information about a post, including the URL, data, tags and the body of the post.

I was naïvely saving each of these objects into an array called `all_posts`, and displaying them on the page as follows:

{% raw %}
```html
<ol class="untagged_posts">
  <li ng-repeat="post in all_posts" ng-hide="{{post.tags.length}}">
    <a href="{{post.post_url}}">{{post.post_url}}</a>
  </li>
</ol>
```
{% endraw %}

The `ng-repeat` loop goes through every post, and hides it if the length of the `tags` attribute is non-zero (that is, if the post is tagged). The untagged posts are shown as list items with the appropriate link.

This means that the `all_posts` array includes an object for every post on a blog. When it's finished, this array is hundreds of megabytes in size. I'm sure this was causing memory problems, especially in mobile browsers.

In the update, the `all_posts` array is filtered to only include untagged posts. Objects for tagged posts are discarded immediately. I have two utility functions:

{% code lang="javascript" names="0:post_is_untagged 1:post 5:filter_untagged_posts 6:posts" %}
var post_is_untagged = function(post) {
    return !post.tags.length;
}

var filter_untagged_posts = function(posts) {
    return posts.filter(post_is_untagged);
}
{% endcode %}

which are applied to all the post objects I receive from the Tumblr API. Then I renamed the array to `untagged_posts`, and slightly simplified the HTML:

{% raw %}
```html
<ol class="untagged_posts">
  <li ng-repeat="post in untagged_posts">
    <a href="{{post.post_url}}">{{post.post_url}}</a>
  </li>
</ol>
```
{% endraw %}

## Trim the information saved in `untagged_posts`

Discarding all the tagged posts reduces memory usage, but I was still populating an array with hundreds of large objects. Once I know that a post is untagged, then all I really need is the URL.

So I refined `filter_untagged_posts` so that all I save is the URL, and every other attribute gets discarded:

{% code lang="javascript" names="0:filter_untagged_posts 1:posts 2:untagged_posts 6:trimmed_urls 7:p" %}
var filter_untagged_posts = function(posts) {
    untagged_posts   = posts.filter(post_is_untagged);
    var trimmed_urls = [];

    for (var p in untagged_posts) {
        trimmed_urls.push(untagged_posts[p].post_url);
    }

    return trimmed_urls
}
{% endcode %}

Now the `untagged_posts` array only includes URLs, and the HTML can be simplified even further:

{% raw %}
```html
<ol class="untagged_posts">
  <li ng-repeat="url in untagged_posts">
    <a href="{{url}}">{{url}}</a>
  </li>
</ol>
```
{% endraw %}

An array of thousands of URLs is still quite large, but nowhere near as large as if I was still storing the body of each post. I think this should make a big difference to performance.

Ideally, I'd never receive this information from the API at all. It's a waste of bandwidth at both ends. Other APIs have filtering parameters, where you can choose exactly what gets sent ([Stack Exchange][se] or [Wolfram Alpha][wa] are two examples), and I'd like to have this for Tumblr. Just not getting the body of each post would save a lot of bandwidth.

I've made a feature request to Tumblr, so hopefully this will show up soon.

## Cosmetic changes

I've made a few tweaks to clean up the site, especially in mobile browsers. Most of this is trimming cruft, tweaking the header to match this site and catching common typos in the URL field.

[se]: http://api.stackexchange.com/docs/filters
[wa]: http://products.wolframalpha.com/api/documentation.html#8

[post1]: http://finduntaggedtumblrposts.com/
