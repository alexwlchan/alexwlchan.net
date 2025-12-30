---
layout: page
title: Tags
nav_section: tags
---
{% assign site_tags = site.data['tag_tally'] | sort %}

<style>
  #tags {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-column-gap: var(--grid-gap);
  }
  
  #tags dt {
    text-align: right;
  }
  
  #tags dd {
    margin: 0;
  }

  #tags a:visited {
    color: var(--link-color);
  }

  /* These controls are hidden by default, and only appear when the
   * JavaScript loads on the page -- if the JavaScript doesn't work,
   * you won't see any controls. */
  #tagSortingControls {
    display: none;
  }

  select {
    font-size: 1em;
  }
</style>

<p id="tagSortingControls"></p>

TODO: Add a heading, add remaining descripitons, highlight popular tags, remove namespaced tags that aren't used much

<dl id="tags">
  {% for tag_info in site_tags %}
    {% assign tag_name = tag_info[0] %}
    {% assign tag_count = tag_info[1]['posts'].size %}
    <dt
      data-tag-name="{{ tag_name }}"
      data-tag-count="{{ tag_count }}"
    >
      {% include tag_link.html %}
    </dt>
    <dd
      data-tag-name="{{ tag_name }}"
      data-tag-count="{{ tag_count }}"
    >
      {{- tag_count }} post{% if tag_count > 1 %}s{% endif -%}
      {% if tag_info[1]['description'] %}
      about {{ tag_info[1]['description'] -}}
      {%- endif -%}
    </dd>
  {% endfor %}
</dl>

<script>
  const tagSortOptions = [
    {
      id: 'nameAtoZ',
      label: 'tag name (A to Z)',
      compareFn: (a, b) => {
        const aName = a.getAttribute("data-tag-name");
        const bName = b.getAttribute("data-tag-name");
        return aName > bName ? 1 : -1;
      },
    },
    {
      id: 'nameZtoA',
      label: 'tag name (Z to A)',
      compareFn: (a, b) => {
        const aName = a.getAttribute("data-tag-name");
        const bName = b.getAttribute("data-tag-name");
        return aName < bName ? 1 : -1;
      },
    },
    // When sorting by frequency of use, if there are lots of tags that
    // have been used the same number of times, we sort that sublist A to Z.
    {
      id: 'countMostToLeast',
      label: '# of uses (most to least)',
      compareFn: (a, b) => {
        const aName = a.getAttribute("data-tag-name");
        const bName = b.getAttribute("data-tag-name");

        const aCount = Number(a.getAttribute("data-tag-count"));
        const bCount = Number(b.getAttribute("data-tag-count"));

        return aCount !== bCount
          ? bCount - aCount
          : (aName > bName ? 1 : -1);
      }
    },
    {
      id: 'countLeastToMost',
      label: '# of uses (least to most)',
      compareFn: (a, b) => {
        const aName = a.getAttribute("data-tag-name");
        const bName = b.getAttribute("data-tag-name");

        const aCount = Number(a.getAttribute("data-tag-count"));
        const bCount = Number(b.getAttribute("data-tag-count"));

        return aCount !== bCount
          ? aCount - bCount
          : (aName > bName ? 1 : -1);
      },
    },
    // We need to assign a random weight for each tag, and that weight
    // needs to be consistent during the sort (or the list might not be
    // shuffled properly), but we don't care about being able to
    // e.g. seed the RNG or reproduce a random order later.
    //
    // This is just for casual exploration.
    {
      id: 'random',
      label: 'random',
      compareFn: (a, b) => {
        const aName = a.getAttribute("data-tag-name");
        const bName = b.getAttribute("data-tag-name");

        randomWeights[aName] ??= Math.random();
        randomWeights[bName] ??= Math.random();

        return randomWeights[aName] - randomWeights[bName];
      }
    }
  ];

  var randomWeights = {};

  /* Apply a sort order to a list of items.
   *
   * This takes three parameters:
   *
   *    - items (Array[T]): the list of photos to get
   *    - sortOptions: the list of sort options
   *    - sortOrderId (string|null): the sort order ID selected by the user
   *
   * It returns an object with two fields:
   *
   *    - sortedItems: the list of photos, with the sort applied
   *    - appliedSortOrder: the sort order that was applied
   *
   */
  function sortItems(props) {
    const { items, sortOptions, sortOrderId } = props;

    // What sort order are we using?
    //
    // Try to find a matching sort option in those we know how to handle;
    // if the user didn't pass an explicit sort order or we don't recognise
    // the ID, we just use the default sort.
    const defaultSort = sortOptions[0];
    const selectedSort =
      sortOptions.find(s => s.id === sortOrderId) || defaultSort;

    console.debug(`Selected sort: ${JSON.stringify(selectedSort)}`);

    // Now apply the sort to the list of items.
    const sortedItems = items.sort(selectedSort.compareFn);

    return { sortedItems, appliedSortOrder: selectedSort };
  }

  /* Create the controls the user can use to choose their sort options.
   *
   * The final HTML will be a dropdown, something like:
   *
   *     <select id="sortControls">
   *       <option id="postsMostToLeast">number of posts (most to least)</option>
   *       <option id="postsLeastToMost">number of posts (least to most)</option>
   *       …
   *     </select>
   */
  const SortControls = (sortOptions, sortOrderId) => `
    Sort by:
    <select id="sortOrder" onchange="updateSortOrder()">
      ${
        sortOptions
          .map(({ id, label }) => `
            <option value="${id}" ${id === sortOrderId ? 'selected' : ''}>
              ${label}
            </option>
          `)
          .join("")
      }
    </select>
  `;

  /* Get/set the currently selected sort order in this dropdown. */
  function getSelectedSortOrder() {
    return document.querySelector("select#sortOrder").value;
  }

  /* Reload the page with the new sort. */
  function updateSortOrder() {
    window.location.search =
      updateSortQueryString({
        queryString: window.location.search,
        sortOrderId: getSelectedSortOrder(),
      });
  }

  /* Update the query string for this URL with a new sort order. */
  function updateSortQueryString(props) {
    const { queryString, sortOrderId } = props;

    const params = new URLSearchParams(queryString);
    params.set("sortOrder", sortOrderId);

    return params.toString();
  }

  window.addEventListener("DOMContentLoaded", function() {
    const params = new URLSearchParams(window.location.search);

    // Apply sorting, e.g. by name or number of uses.
    //
    // This means actually sorting the tags, and adding the list of
    // sort options to the page.
    const sortOrderId = params.get("sortOrder");
    
    const tagsElem = document.querySelector("#tags");

    const tagElements = [...tagsElem.querySelectorAll("dt")];

    const { sortedItems, appliedSortOrder } = sortItems({
      items: tagElements, sortOptions: tagSortOptions, sortOrderId
    });

    sortedItems.forEach(dtElem => {
      const ddElem = [...tagsElem.querySelectorAll("dd")].filter(
        dd => dd.getAttribute("data-tag-name") === dtElem.getAttribute("data-tag-name")
      )[0];
      tagsElem.appendChild(dtElem);
      tagsElem.appendChild(ddElem);
    });

    document.querySelector('#tagSortingControls').innerHTML =
      SortControls(tagSortOptions, appliedSortOrder.id);
    document.querySelector('#tagSortingControls').style.display = 'block';
  });
</script>
