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

  // And do the same for the "jump to" elements
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
}

window.onload = function() {
  document.getElementById("tag_filter").style.display = "block";
};
