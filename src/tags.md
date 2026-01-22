---
layout: page
title: Tags
nav_section: tags
---
{% set visible_tags = site.data['tag_tally'].items()|sort %}

<style>
  #tags {
    list-style-type: none;
    padding: 0;
    columns: 1;
    line-height: 1.7em;
  }

  #tags a:visited {
    color: var(--link-color);
  }

  #tagSortingControls {
    display: none;
  }

  @media screen and (min-width: 518px) {
    #tags {
      columns: 2;
    }
  }

  @media screen and (min-width: 747px) {
    #tags {
      columns: 3;
    }
  }

  select {
    font-size: 1em;
  }
</style>

<p id="tagSortingControls"></p>

<ul id="tags">
  {% for tag_name, tagged_pages in visible_tags %}
    <li
      data-tag-name="{{ tag_name }}"
      data-tag-count="{{ tagged_pages|count }}"
    >
      {% include "partials/tag_link.html" %} ({{ tagged_pages|count }})
    </li>
  {% endfor %}
</ul>

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

    const tagElements = Array.from([...document.querySelectorAll("#tags > li")]);

    const { sortedItems, appliedSortOrder } = sortItems({
      items: tagElements, sortOptions: tagSortOptions, sortOrderId
    });

    sortedItems.forEach(elem =>
      document.querySelector("#tags").appendChild(elem)
    );

    document.querySelector('#tagSortingControls').innerHTML =
      SortControls(tagSortOptions, appliedSortOrder.id);
    document.querySelector('#tagSortingControls').style.display = 'block';
  });
</script>