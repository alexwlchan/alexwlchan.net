---
layout: page
title: Articles
nav_section: articles
---
There's nothing here yet, but soon it'll have a list of things I've written.

<style type="x-text/scss">
  {% for article in site.articles %}
    {% if article.colors.index_light %}
      #article-{{ article.slug }}.article_card {
        @include card_light_styles({{ article.colors.index_light }});
      }
    {% elsif article.colors.css_light %}
      #article-{{ article.slug }}.article_card {
        @include card_light_styles({{ article.colors.css_light }});
      }
    {% endif %}
  {% endfor %}

  @media (prefers-color-scheme: dark) {
    {% for article in site.articles %}
      {% if article.colors.index_dark %}
        #article-{{ article.slug }}.article_card {
          @include card_dark_styles({{ article.colors.index_dark }});
        }
      {% elsif article.colors.css_dark %}
        #article-{{ article.slug }}.article_card {
          @include card_dark_styles({{ article.colors.css_dark }});
        }
      {% endif %}
    {% endfor %}
  }
</style>


<ul id="list_of_articles">
{% for article in site.articles reversed %}

  <li class="article_card" id="article-{{ article.slug }}">
    {% include article_card.html %}
  </li>
{% endfor %}
</ul>
