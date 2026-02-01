---
layout: topic
title: Books I've read
---
I love reading!
I always have a book on the go, and I can often be found between the shelves of my local library.
I worked as a software developer at [Wellcome Collection](https://wellcomecollection.org) for seven years, where I got to see what makes a library tick.

I'm also a regular attendee of the [London Ace Book Club](https://aceandarolondon.org.uk/bookclub/), and have been since it started running in October 2022.
It's where I met my partner; we bonded over our love of books.

This page is where I keep notes on all the books I've read:



<style>
  .reviews {
    list-style-type: "";
    padding: 0;
    margin:  0;
  }

  .reviews > li {
    display: grid;
    grid-template-columns: 85px 1fr;
    column-gap: var(--grid-gap);
    row-gap: 7px;
    margin-top: 1em;
    
    /* If there's no summary, tighten the gap between the title and rating */
    &.ns {
      row-gap: 3px;
    }
    
    /* cover image */
    a:first-child {
      grid-row: 1 / span 2;
      
      figure {
        height: 75px;
        margin: 0;
      }
      
      &:hover img {
        outline: 3px solid var(--c-lt);
      }
    }
    
    @media screen and (prefers-color-scheme: dark) {
      a:first-child:hover img {
        outline: 3px solid var(--c-dk);
      }
    }
    
    p {
      margin: 0;
      grid-column: 2 / 2;
    }
    
    /* book title */
    p:nth-child(2) {
      margin-top: auto;
    }
    
    /* summary */
    p:nth-child(3) {
      font-size: 85%;
      line-height: 1.45em;
      margin-bottom: auto;
    }
    
    /* star rating */
    .sr {
      letter-spacing: 0.1em;
      white-space: nowrap;
    }
  }
</style>

{% from "partials/star_rating.html" import star_rating %}
{% from "partials/topic_entries.html" import topic_section %}
{% set featured = site.articles
  | selectattr("template_name", "eq", "post.html")
  | selectattr("is_featured")
  | selectattr("topic", "eq", "Books I've read")
  | sort(attribute="date", reverse=True) %}

<div id="topic_entries">
  {{ topic_section(featured, "article_cards") }}

  {% set per_year_reviews =
      site.book_reviews
        | sort(attribute="review.date_read", reverse=True)
        | groupby("review.date_read.year")
        | sort(reverse=True) %}

  {%- for year, reviews in per_year_reviews -%}
    <section>
      <div>
        <h2>Books I read in {{ year }}</h2>
        <p>
          {%- if site.time.year == year -%}
          I’ve read {{ reviews|count }} book{% if reviews|count > 1 %}s{% endif %} so far this year:
          {%- else -%}
          I read {{ reviews|count }} book{% if reviews|count > 1 %}s{% endif %}:
          {%- endif %}
        </p>
        <ul class="reviews">
        {% for rev in reviews %}
        <li{% if not rev.review.summary %} class=" ns"{% endif %} style="--c-lt: {{ rev.colors.css_light }}; --c-dk: {{ rev.colors.css_dark }}">
          <a href="{{ rev.url }}">
          {#-
            The cover images get renamed, similar to the article cards,
            to reduce the overall size of the page.
            
            The bk_index counts the order in which I read the book that
            year, and then they're filed in a per-year folder.
            
            For example: images/b26/4 is the 4th book I read in 2026.
            
            TODO: We can make the <picture> quite a bit shorter here,
            and replace it with 1x/2x for the sizes attribute
          -#}
          <figure>
            {% set bk_index = (reviews|count) - loop.index0 %}
            {% set parent = "/images/" + rev.review.date_read.year|string %}
            {% set dst_prefix = "b/" + (rev.review.date_read.year-2000)|string + "/" + bk_index|string %}
            {%- set cover_image -%}
            {%
              picture
              filename=rev.cover_image.name
              height="75"
              parent=parent
              alt=""
              loading="lazy"
              dst_prefix=dst_prefix
              max_pixel_density=2
              size_based_on="density"
            %}
            {%- endset -%}
            {{- cover_image -}}
          </figure>{{- "" -}}
          </a>
          
          {{- "" -}}
          
          <p>
            <a href="{{ rev.url }}"><em>{{ rev.book.title }}</em></a>, {{ rev.attribution_line }} 
            {%- if rev.review.did_not_finish -%}
              {{ " " }}(did not finish)
            {%- endif -%}
          </p>
          
          {{- "" -}}
          
          {%- set description -%}
          <p>
            {%- if rev.review.summary -%}
              {{- rev.review.summary | smartify -}}
              {%- with rating = (rev.review.rating, 5) -%}
                {%- include "partials/star_rating.html" -%}
              {%- endwith -%}
              {% if rev.review.rating %}
                {{ " " }}({{ star_rating(rev.review.rating) }}).
              {% endif %}
            {%- elif rev.review.rating -%}
              {{- star_rating(rev.review.rating) -}}
            {%- endif -%}
          </p>
          {%- endset -%}
          
          {{- description
              | replace('<p><span class="sr">★★☆☆☆</span></p>',
                        '<p class="sr">★★☆☆☆</p>')
              | replace('<p><span class="sr">★★★☆☆</span></p>',
                        '<p class="sr">★★★☆☆</p>')
              | replace('<p><span class="sr">★★★★☆</span></p>',
                        '<p class="sr">★★★★☆</p>')
              | replace('<p><span class="sr">★★★★★</span></p>',
                        '<p class="sr">★★★★★</p>')
          -}}
        </li>
        {% endfor %}
        </ul>
      </div>
    </section>
  {%- endfor -%}
</div>

