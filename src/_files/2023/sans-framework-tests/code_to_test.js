function isUndefined(t) {
  return typeof t === 'undefined';
}

function isNotUndefined(t) {
  return !isUndefined(t);
}

/** Creates a label to describe the current publication year filter. e.g.
  *
  *     published between 2001 and 2002
  *     published in 2004
  *     published before 1990
  *
  */
function createPublicationYearLabel(range) {
  const { beforeYear, afterYear } = range;

  const hasAfterYear = isNotUndefined(afterYear);
  const hasBeforeYear = isNotUndefined(beforeYear);

  const thisYear = new Date().getUTCFullYear().toString();

  const label = hasAfterYear && hasBeforeYear && beforeYear === afterYear
    ? `in ${afterYear}`
    : hasAfterYear && hasBeforeYear
    ? `between ${afterYear} and ${beforeYear}`
    : hasAfterYear && afterYear == thisYear
    ? `in ${thisYear}`
    : hasAfterYear
    ? `after ${afterYear}`
    : `before ${beforeYear}`;

  return `published ${label}`;
}

/** Parses an author string into individual authors, e.g.
  *
  *     John Smith and Sarah Jones
  *      ~> ['John Smith', 'Sarah Jones']
  *
  */
function parseAuthorNames(authors) {
  if (authors === 'Alan & Maureen Carter') {
    return ['Alan Carter', 'Maureen Carter'];
  }

  if (authors === 'Stephen Hawking with Leonard Mlodinow') {
    return ['Stephen Hawking', 'Leonard Mlodinow'];
  }

  return authors
    .split(/,|&| and /)
    .map(s => s.trim())
    .filter(s => s.length > 0);
}

/** Returns true if a given book matches the specified filters.
  *
  * Here the `filters` has the following structure:
  *
  *     {
  *       authors: string[],
  *       publicationYear: {
  *         before: number | undefined,
  *         after: number | undefined,
  *       },
  *       starRating: number | undefined,
  *       tags: string[],
  *     };
  */
function matchesFilters(book, filters) {

  // It's sufficient to match a single author in the list.
  const authors = parseAuthorNames(book.getAttribute('data-book-authors'));

  const matchesAuthorFilter =
    filters.authors.length === 0 ||
    authors.some(a => filters.authors.indexOf(a) !== -1);

  // The publication year has to fall within the defined range
  const publicationYear = Number(book.getAttribute('data-book-publication-year'));

  const matchesPublicationYearAfterFilter =
    isUndefined(filters.publicationYear.after) ||
    filters.publicationYear.after <= publicationYear;

  const matchesPublicationYearBeforeFilter =
    isUndefined(filters.publicationYear.before) ||
    publicationYear <= filters.publicationYear.before;

  // The star rating has to be equal to or higher than the filtered rating
  const starRating = Number(book.getAttribute('data-review-rating'));

  const matchesStarRatingFilter =
    isUndefined(filters.starRating) ||
    filters.starRating <= starRating;

  // It has to match all the tags specified
  const tags = new Set(book.getAttribute('data-review-tags').split(' '));

  const matchesTagsFilter =
    filters.tags.length === 0 ||
    filters.tags.every(t => tags.has(t));

  return (
    matchesAuthorFilter &&
    matchesPublicationYearAfterFilter &&
    matchesPublicationYearBeforeFilter &&
    matchesStarRatingFilter &&
    matchesTagsFilter
  );
}

function createSummaryMessage(options) {
	const { finishedCount, year, isThisYear } = options;

	if (isThisYear) {
		return `${year}: I’ve read ${finishedCount} book${finishedCount > 1 ? 's' : ''} so far`;
	} else {
		return `${year}: I read ${finishedCount} book${finishedCount > 1 ? 's' : ''}`;
	}
}
