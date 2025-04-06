---
layout: page
title: ""
colors:
  css_light: "#17823e"
  css_dark:  "#26d967"
footer:
  hide_newsletter: true
---

<style type="x-text/scss">
  @use "components/article_cards";
  @use "utils/functions.scss" as *;

  @function create_leaf_svg($fill) {
    $fill: str-replace("#{$fill}", '#', '%23');
    $output: '<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" viewBox="0 0 98 98" width="50px">' +
             "<path fill=\"#{$fill}\" " +
             'd="M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z"/>' +
             '</svg>';
    @return str-replace($output, '"', '%22');
  }

  hr {
    height: 50px;
    width: 50px;

    $light-svg-url: create_leaf_svg(rgba(#17823e, 0.2));
    $dark-svg-url:  create_leaf_svg(rgba(#26d967, 0.6));

    --hr-background-image: url("data:image/svg+xml;charset=UTF-8,#{$light-svg-url}");

    @media (prefers-color-scheme: dark) {
      --hr-background-image: url("data:image/svg+xml;charset=UTF-8,#{$dark-svg-url}");
    }
  }

  #headshot {
    margin-left:   var(--default-padding);
    margin-bottom: var(--default-padding);
  }

  #headshot .picture_wrapper,
  #headshot img {
    border-radius: 50%;
  }

  @media screen and (min-width: 500px) {
    main {
      padding-top: calc(1.5 * var(--default-padding));
    }

    #headshot {
      float: right;
    }
  }

  @media screen and (max-width: 500px) {
    #headshot {
      display: block;
      margin-top: var(--default-padding);
      margin-left:  auto;
      margin-right: auto;
    }
  }
</style>

**Hi, I’m Alex. I'm a software developer, writer, and hand crafter from the UK.**

<div id="headshot">
{%
  picture
  filename="profile_green_square.jpg"
  parent="/images"
  width="230"
  alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
  class="rounded_corners"
%}
</div>

I build systems for **digital preservation** -- making sure that digital archives remain safe and accessible into the far future.
Currently I think about photos at <a href="https://www.flickr.org">the Flickr Foundation</a>, and before that I helped build services to store and search the museum and library collections at <a href="https://wellcomecollection.org/">Wellcome Collection</a>.

I enjoy **writing**, and I've been posting at this domain since 2012.
I write about a variety of non-fiction topics, with a particular focus on software development.
If you want to know what's on my mind, check out [the articles I've written](/articles/), [the talks I've given](/tags/talks/), and [the lessons I've learned](/til/).

In my free time, I enjoy doing art and simple **hand crafts** to relax.
I've had a lot of fun doing [cross stitch](/tags/cross-stitch/), origami and paper craft, and doodling sketches of implausible sci-fi vehicles.

I'm **queer** and **trans**.
My pronouns are "they" or "she".

This website is a place to share stuff I find interesting or fun.
I hope you like it!



---



## Favourite articles

Here are some of my favourite things [that I've written](/articles/):

{% comment %}
  This component shows 6 featured articles.

  To keep things somewhat interesting, I have more than 6 such articles
  and I display a random selection.

  - The Jekyll build will pick a sample of 6 every time it's built
  - JavaScript on the page will shuffle the list on page reloads

  New articles always appear in the top left, but other articles can
  rotate around them.

{% endcomment %}

{% assign featured_articles = site.posts | where: "index.feature", true %}

{% assign new_articles = featured_articles | where: "is_new", true %}

{% assign new_count = new_articles | size %}
{% assign sample_size = 6 | minus: new_count %}
{% assign sample_of_articles = featured_articles | sample: sample_size %}

<script>
  function CardImage(card) {
    const yr = card.y - 2000;
    const prefix = card.p;

    if (card.fm === 'JPEG') {
      var suffix = '.jpg';
      var mimeType = 'image/jpg';
    } else {
      var suffix = '.png';
      var mimeType = 'image/png';
    }

    return `
      <div class="c_im_w${card.n ? ' n' : ''}">
        <picture>
          <source
            srcset="/c/${yr}/${prefix}_365w${suffix} 365w,
                    /c/${yr}/${prefix}_730w${suffix} 730w,
                    /c/${yr}/${prefix}_302w${suffix} 302w,
                    /c/${yr}/${prefix}_604w${suffix} 604w,
                    /c/${yr}/${prefix}_405w${suffix} 405w,
                    /c/${yr}/${prefix}_810w${suffix} 810w"
            sizes="(max-width: 450px) 405px, 405px"
            type="${mimeType}"
          >
          <source
            srcset="/c/${yr}/${prefix}_365w.avif 365w,
                    /c/${yr}/${prefix}_730w.avif 730w,
                    /c/${yr}/${prefix}_302w.avif 302w,
                    /c/${yr}/${prefix}_604w.avif 604w,
                    /c/${yr}/${prefix}_405w.avif 405w,
                    /c/${yr}/${prefix}_810w.avif 810w"
            sizes="(max-width: 450px) 405px, 405px"
            type="image/avif"
          >
          <source
            srcset="/c/${yr}/${prefix}_365w.webp 365w,
                    /c/${yr}/${prefix}_730w.webp 730w,
                    /c/${yr}/${prefix}_302w.webp 302w,
                    /c/${yr}/${prefix}_604w.webp 604w,
                    /c/${yr}/${prefix}_405w.webp 405w,
                    /c/${yr}/${prefix}_810w.webp 810w"
            sizes="(max-width: 450px) 405px, 405px"
            type="image/webp"
          >
          <img src="/c/${yr}/${prefix}_365w.jpg" alt="" loading="lazy">
        </picture>
        ${card.n ? '<div class="new_banner">NEW</div>' : ''}
      </div>
    `;
  }

  function ArticleCard(card) {
    return `
      <li
        class="card"
        style="
          ${card.cl ? `--c-lt: #${card.cl}` : ''};
          ${card.cd ? `--c-dk: #${card.cd}` : ''};
        "
      >
        <a href="/${card.y}/${card.s}/">
          ${CardImage(card)}
          <div class="c_meta">
            <p class="c_title">
              ${card.t}
            </p>
            ${
              typeof card.d !== 'undefined'
                ? `<p class="c_desc">${card.d}</p>`
                : ''
            }
          </div>
        </a>
      </li>
    `;
  }

  {%- capture featuredArticlesJson -%}
    [
      {% comment %}
        cl = color light
        cd = color dark
        new = is new?
        t = title
        y = year
        s = slug
        p = prefix
        fm = image format
        d = descritpion
      {% endcomment %}
      {% for article in featured_articles %}
        {
          "cl": {{ article.card.color_lt | replace: "#", "" | jsonify }},
          "cd": {{ article.card.color_dk | replace: "#", "" | jsonify }},
          {% if article.is_new %}
          "n": {{ article.is_new }},
          {% endif %}
          "t": {{ article.title | markdownify_oneline | cleanup_text | jsonify }},
          "y": {{ article.date | date: "%Y" }},
          "s": {{ article.slug | jsonify }},
          "p": {{ article.card.index_prefix | jsonify }},
          "fm": {{ article.card.index_image.format | jsonify }},
          {% if article.summary %}
            "d": {{ article.summary | markdownify_oneline | cleanup_text | jsonify }}
          {% endif %}
        }
        {% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  {%- endcapture -%}

  const featuredArticles = {{ featuredArticlesJson | compact_json }};

  window.addEventListener("DOMContentLoaded", function() {
    const newArticles = featuredArticles
      .filter(card => typeof card.n !== 'undefined');
    const randomArticles = featuredArticles
      .filter(art => !newArticles.includes(art))
      .sort(() => 0.5 - Math.random())
      .slice(0, 6);

    document.querySelector("#featured_articles").innerHTML =
      newArticles.concat(randomArticles)
        .slice(0, 6)
        .map(ArticleCard)
        .join("");
  });
</script>

<ul class="article_cards" id="featured_articles">
  {% for article in new_articles %}
    {% include article_card.html %}
  {% endfor %}
  {% for article in sample_of_articles %}
    {% include article_card.html %}
  {% endfor %}
</ul>

Here are some of the topics I write about:

<ul class="dot_list" id="popular_tags">
  {% for tag_name in site.data['popular_tags'] %}
    <li>{% include tag_link.html %}</li>
  {% endfor %}
</ul>

<style>
  #popular_tags a:visited {
    color: var(--link-color);
  }
</style>



---

{% include newsletter.html %}
