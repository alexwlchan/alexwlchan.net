---
layout: page
title: ""
colors:
  css_light: "#17823e"
  css_dark:  "#26d967"
---

<style type="x-text/scss">
  @use "components/article_cards";

  hr {
    height: 50px;
    width:  50px;

    --hr-background-image: url("data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 x=%220px%22 y=%220px%22 viewBox=%220 0 98 98%22 width=%2250px%22><path fill=\%22%2317823e33\%22 d=%22M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z%22/></svg>");

    @media (prefers-color-scheme: dark) {
      --hr-background-image: url("data:image/svg+xml;charset=UTF-8,<svg xmlns=%22http://www.w3.org/2000/svg%22 x=%220px%22 y=%220px%22 viewBox=%220 0 98 98%22 width=%2250px%22><path fill=\%22%2326d96799\%22 d=%22M30.636,61.596c-1.006,1.497-1.859,2.997-2.56,4.5c-3.046,6.531-3.178,13.179-0.396,19.941  c0.536,1.304-0.087,2.797-1.391,3.333c-1.305,0.536-2.797-0.087-3.333-1.391c-3.354-8.155-3.195-16.171,0.476-24.045  c3.45-7.397,10.028-14.608,19.732-21.633c2.324-1.893,4.818-3.785,7.483-5.678c1.069-0.759,1.321-2.241,0.562-3.31  c-0.759-1.069-2.241-1.321-3.31-0.561C37.653,40.026,29.77,47.454,24.243,55.01c-2.331-13.176-0.587-23.597,5.221-31.032  c8.019-10.267,24.155-15.49,47.983-15.54c-0.048,23.828-5.272,39.965-15.538,47.984C54.43,62.264,43.927,63.992,30.636,61.596z%22/></svg>");
    }
  }

  img#headshot {
    border-radius: 50%;
    margin-left:   var(--default-padding);
    margin-bottom: var(--default-padding);
  }

  @media screen and (min-width: 500px) {
    main {
      padding-top: calc(1.5 * var(--default-padding));
    }

    img#headshot {
      margin-top: -3em;
      float: right;
    }
  }

  @media screen and (max-width: 500px) {
    img#headshot {
      display: block;
      margin-top: var(--default-padding);
      margin-left:  auto;
      margin-right: auto;
    }
  }

  #popular_tags a {
    white-space: nowrap;
  }
</style>

**Hi, I’m Alex. Welcome to my website!**

{%
  picture
  filename="profile_green_sq.jpg"
  id="headshot"
  parent="/images"
  width="230"
  alt="A selfie! I’m smiling at the camera, wearing a green dress, and sitting in front of a large amount of green foliage. It’s a sunny day and shining both on the side of my face and the plants."
  class="rounded_corners"
%}

I'm a software developer, writer, and a hand crafter, and I live in the UK.
In my day job I build software for digital preservation, and I think a lot about archiving and long-term systems.

This website is where I share stuff I find interesting or fun.
That includes notes on technical problems I've solved, personal reflections or thoughts, and fun toys that I've built.

I'm queer and trans, and my pronouns are "they" or "she".

I hope you like it!



---



## Favourite articles

Here are some of my favourite things [that I've written](/articles/):

<ul class="acards" id="featured_articles">
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
    const yr = card.y;

    const suffix = card.fm === 0 ? '.jpg' : '.png';
    const mimeType = card.fm === 0 ? 'image/jpg' : 'image/png';

    const prefix = card.s.slice(0, card.p);
    const imPrefix = `/c/${yr}/${prefix}`;

    const ws = [
      365, 365 * 2,  /* 2-up column => ~365px wide */
      302, 302 * 2,  /* 3-up column => ~302px wide */
      405, 405 * 2   /* 1-up column => ~405px wide */
    ];
    const avif    = ws.map(s => `${imPrefix}_${s}w.avif ${s}w`).join(", ");
    const webp    = ws.map(s => `${imPrefix}_${s}w.webp ${s}w`).join(", ");
    const primary = ws.map(s => `${imPrefix}_${s}w${suffix} ${s}w`).join(", ");

    // See comment in `article_card.html`
    const sizes = "(max-width: 450px) 100vw,(max-width:1000px) 50vw,300px";

    return `
      <div class="c_im${card.n ? ' n' : ''}">
        <picture>
          <source srcset="${avif}"    sizes="${sizes}" type="image/avif">
          <source srcset="${webp}"    sizes="${sizes}" type="image/webp">
          <source srcset="${primary}" sizes="${sizes}" type="${mimeType}">
          <img src="/c/${yr}/${card.p}_365w.jpg" alt="" loading="lazy">
        </picture>
        ${card.n ? '<div class="new_banner">NEW</div>' : ''}
      </div>
    `;
  }

  function ArticleCard(card) {
    return `
      <li
        style="
          ${card.cl ? `--lt: #${card.cl}` : ''};
          ${card.cd ? `--dk: #${card.cd}` : ''};
        "
      >
        <a href="/${card.y + 2000}/${card.s}/">
          ${CardImage(card)}
          <div class="c_meta">
            <p class="c_t">${card.t}</p>
            ${typeof card.d !== 'undefined' ? `<p class="c_d">${card.d}</p>` : ''}
          </div>
        </a>
      </li>
    `;
  }

  {% comment %}
    cl = color light
    cd = color dark
    n = is new?
    t = title
    y = year - 2000
    s = slug
    p = length of prefix
    fm = image format (0 = JPEG, 1 = PNG)
    d = description
  {% endcomment %}
  const keys = ["cl","cd","n","t","y","s","p","fm","d"];

  {%- capture featuredArticlesJson -%}
    [
      {% for article in featured_articles %}
        [
          {{ article.card.color_lt | replace: "#", "" | jsonify }},
          {{ article.card.color_dk | replace: "#", "" | jsonify }},
          {% if article.is_new %}1{% else %}0{% endif %},
          {{ article.title | markdownify_oneline | cleanup_text | jsonify }},
          {{ article.date | date: "%Y" | minus: 2000 }},
          {{ article.slug | jsonify }},
          {{ article.card.short_name | size }},
          {% if article.card.index_image.format.mime_type == "image/jpeg" %}
            0
          {% else %}
            1
          {% endif %},
          {% if article.summary %}
            {{ article.summary | markdownify_oneline | cleanup_text | replace: ' class="language-plaintext highlighter-rouge"', "" | jsonify }}
          {% else %}
            ""
          {% endif %}
        ]
        {% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  {%- endcapture -%}

  const featuredArticlesList = {{ featuredArticlesJson | minify_json }};

  const featuredArticles = featuredArticlesList.map(values =>
    keys.reduce((obj, key, index) => ({ ...obj, [key]: values[index] }), {})
  );

  window.addEventListener("DOMContentLoaded", function() {
    const newArticles = featuredArticles
      .filter(art => art.n === 1);

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
