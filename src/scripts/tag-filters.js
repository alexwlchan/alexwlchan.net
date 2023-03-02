function applyTagFilters() {
  const selectedTag = document.getElementById("tag_selection").value;
  console.log(`Filtering to posts tagged with ${selectedTag}`);

  let visibleYears = new Set();

  // First we go through all the cards on the page, and we work out which
  // posts we're going to show.  We also track the associated year on
  // each of the cards, so we know which years to allow jumping to.
  for (card of document.querySelectorAll(".card")) {
    const cardTags = card.getAttribute("data-post-tags").split(" ");

    const shouldShowCard = Boolean(
      selectedTag === "_nofilter_" ||
      cardTags.indexOf(selectedTag) != -1
    );

    if (shouldShowCard) {
      visibleYears.add(card.getAttribute("data-post-year"));
    }

    card.style.display = shouldShowCard ? "list-item" : "none";
  }

  // Then we go through the year groups, and we remove any which don't
  // have any cards displaying.
  for (yearGroup of document.querySelectorAll(".year_group")) {
    const thisYear = yearGroup.getAttribute("data-group-year");
    yearGroup.style.display = visibleYears.has(thisYear) ? "block" : "none";
  }

  // And do the same for the "jump to" elements.
  //
  // There's a bit of hackery going on here with the `first_visible_jumpto`
  // class: I want to insert slashes between the years, e.g.
  //
  //      Jump to: 2022 / 2021 / 2020
  //
  // which is being added with the :not(:first-child)::before, similar to
  // the .dot_list style used elsewhere -- but this selector ignores the
  // visibility of the elements.
  //
  // The `first_visible_jumpto` class marks the first visible item in this
  // list, which doesn't get a leading slash.
  let isFirstVisibleJumpTo = true;

  for (jumpToYear of document.querySelectorAll("#jumpto_list li")) {
    const thisYear = jumpToYear.getAttribute("data-jumpto-year");
    jumpToYear.style.display = visibleYears.has(thisYear) ? "inline" : "none";

    if (visibleYears.has(thisYear) && isFirstVisibleJumpTo) {
      jumpToYear.classList.add("first_visible_jumpto");
      isFirstVisibleJumpTo = false;
    } else {
      jumpToYear.classList.remove("first_visible_jumpto");
    }
  }

  // Add a visual style to mark the tag filter as "enabled".
  const tagFilter = document.getElementById("tag_filter");

  if (selectedTag === "_nofilter_") {
    tagFilter.classList.remove("enabled");
  } else {
    tagFilter.classList.add("enabled");
  }

  // Update the page title and URL to match
  const newTitle = selectedTag === "_nofilter_"
    ? "All posts – alexwlchan"
    : `Posts tagged with ${selectedTag} – alexwlchan`;

  const newUrl = selectedTag === "_nofilter_"
    ? "/all-posts/"
    : `/all-posts/?tag=${selectedTag}`;

  document.title = newTitle;

  history.pushState({ source: 'web' }, newTitle, newUrl)
}

// Note: this uses the DOMContentLoaded instead of the load event so
// it doesn't wait for images to finish loading.  I'm hoping this will
// fix issues where clicking to a filtered page can have a delay before
// the filter applies.
//
// See https://developer.mozilla.org/en-US/docs/Web/API/Document/DOMContentLoaded_event
window.addEventListener("DOMContentLoaded", (event) => {
  document.getElementById("tag_filter").style.display = "block";

  // Look for a tag in the URL, if somebody has linked here -- in which
  // case we should apply that filter immediately.
  let queryParams = new URLSearchParams(window.location.search);
  const prefilledTag = queryParams.get("tag");
  if (prefilledTag !== null) {
    document.getElementById("tag_selection").value = prefilledTag;
    applyTagFilters();
  }
});
