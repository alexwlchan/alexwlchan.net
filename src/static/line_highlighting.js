// Helper functions for line highlighting in the per-file view
// in projects.
//
// The line highlighting can specify a single line (`L1`) or
// a range of lines (`L1-3`). This file contains some functions
// to parse/update the URL, and help this process.
//
// These functions are tested by test_line_highlighting.html.

class Highlighter {
  #baseURL;
  
  #anchorLineId = null;
  
  #startHighlightingAt = -1;
  #endHighlightingAt = -1;
  
  constructor(initialURL) {
    const url = new URL(initialURL);
    this.#baseURL = url.origin + url.pathname;
    
    const lineNos = parseFragment(url.hash);
    
    if (lineNos === null) {
      return;
    }
    
    if (lineNos.start === lineNos.end) {
      this.#anchorLineId = lineNos.start;
    }
    
    this.#startHighlightingAt = lineNos.start;
    this.#endHighlightingAt = lineNos.end;
  };
  
  // getFirstHighlightedLine returns the ID of the first line which
  // should have highlighting, if any.
  //
  // This should be called after page load and used to scroll that
  // line into view, in case the fragment is a range of lines that
  // the browser can't select natively.
  getLineToScrollTo() {
    
    // Only a single line was selected in initial URL fragment,
    // or no line was selected; in both cases, do nothing.
    if (this.#startHighlightingAt === this.#endHighlightingAt) {
      return null
    }
    
    return `L${this.#startHighlightingAt}`;
  }
  
  // shouldBeHighlighted reports whether a line should be highlighted
  // or not.
  //
  // When updating the highlighting, call this function for every line.
  shouldBeHighlighted(lineID) {
    const lineNo = Number(lineID.replace('L', ''));
    return this.#startHighlightingAt <= lineNo && lineNo <= this.#endHighlightingAt;
  }
  
  handleClickEvent({ href, shiftKey }) {
    const fragment = parseFragment(href);

    // Skip links that aren't for an #L fragment
    if (fragment === null) {
      return { newURL: null, preventDefault: false, updateHighlighting: false };
    }
    const lineID = fragment.start;
    
    // If you click an already-highlighted line which is the only highlighted
    // line, reset it.
    if (lineID === this.#startHighlightingAt &&
        lineID === this.#endHighlightingAt) {
      this.#startHighlightingAt = -1;
      this.#endHighlightingAt = -1;
      this.#anchorLineId = null;
      return { newURL: this.#baseURL, preventDefault: true, updateHighlighting: true };
    }
    
    // If a click doesn't set the shiftKey, record it as an anchor ID
    // we can use later, update the highlighting, let the browser handle
    // the rest.
    if (!shiftKey || this.#anchorLineId === null) {
      this.#anchorLineId = lineID;
      this.#startHighlightingAt = lineID;
      this.#endHighlightingAt = lineID;
      return { newURL: null, preventDefault: false, updateHighlighting: true };
    }
    
    if (this.#anchorLineId < lineID) {
      this.#startHighlightingAt = this.#anchorLineId;
      this.#endHighlightingAt = lineID;
    } else {
      this.#startHighlightingAt = lineID;
      this.#endHighlightingAt = this.#anchorLineId;
    }
    
    const newURL = `#L${this.#startHighlightingAt}-${this.#endHighlightingAt}`;
    
    return { newURL, preventDefault: true, updateHighlighting: true };
  }
  
  // updateLineHighlighting updates the line highlighting for the page.
  // TODO: This function doesn't handle empty lines with an ellipsis for
  // a line number, but that's fine for now.
  updateLineHighlighting() {
    document.querySelectorAll('.ln').forEach(line => {
      const shouldHighlight = this.shouldBeHighlighted(line.id);
      
      if (shouldHighlight && !line.classList.contains('highlight')) {
        line.classList.add('highlight');
      } else if (!shouldHighlight && line.classList.contains('highlight')) {
        line.classList.remove('highlight');
      }
    });
  }
}

// parseFragment parses line numbers from a URL fragment.
function parseFragment(fragment) {
  if (fragment.startsWith('#')) {
    fragment = fragment.replace(/^#/, '');
  }
  
  if (fragment.match(/^L[0-9]+$/)) {
    lineNo = Number(fragment.replace('L', ''));
    return { start: lineNo, end: lineNo };
  } else if (fragment.match(/^L[0-9]+-[0-9]+$/)) {
    start = Number(fragment.split("-")[0].replace('L', ''));
    end = Number(fragment.split("-")[1]);
    return { start, end };
  } else {
    return null;
  }
}
