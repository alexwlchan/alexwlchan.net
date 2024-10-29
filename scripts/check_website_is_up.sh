#!/usr/bin/env bash
# This is a simple uptime checker for alexwlchan.net.
#
# It checks a number of URLs, to make sure they're resolving.  This is
# a good way to check that Netlify and DNS are set up correctly, and
# I haven't made any stupid mistakes.

set -o errexit
set -o nounset

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Track the overall successes/failures of this function.
#
# When you call the `record_success/failure` functions, they increment
# these variables.  Ideally there'll be 0 failures!
successes=0
failures=0

record_success() {
    ((successes++)) || true
    echo -e "${GREEN}OK:${NC} $1"
}

record_failure() {
    ((failures++)) || true
    echo -e "${RED}Error:${NC} $1" >&2
}

# Check the status of a single URL.
#
# In particular, it checks that:
#
#   * The URL can be retrieved with an HTTP 200 OK, or redirects to
#     a page that does.
#   * The page retrieved from the URL contains the specified text
#
check_url_text() {
    if (( $# != 2 )); then
        echo "Usage: check_url_text <URL> <text>"
        return 1
    fi

    local url="$1"
    local text="$2"

    # Check that we get an HTTP 200.
    #
    # By default we don't follow redirects, but if we get an HTTP 301
    # then we check that the final destination resolves to a 200 OK.
    local http_status=$(curl -s -o /dev/null -w "%{http_code}" "$url")

    if (( http_status == 301 )); then
        local http_status=$(curl -s -L -o /dev/null -w "%{http_code}" "$url")
    fi

    if (( http_status != 200 )); then
        record_failure "HTTP status code $http_status for $url"
        return 0
    fi

    # Use curl to fetch the page content and check if the text is present
    #
    # The -L flag tells curl to follow redirects before getting the
    # contents of the page.
    if curl -s -L "$url" | grep -q "$text"; then
        record_success "$url"
    else
        record_failure "Text \"$text\" not found in $url"
    fi
}

check_url_text "https://alexwlchan.net/"          "Hi, I’m Alex"
check_url_text "https://alexwlchan.net/articles/" "Articles"

for domain in "alexwlchan.net" "www.alexwlchan.net" "alexwlchan.co.uk" "alexwlchan.com"
do
  for protocol in "http" "https"
  do
    check_url_text "$protocol://$domain/" "Hi, I’m Alex"
  done
done

echo "RESULT: $successes successful checks, $failures failed checks"

if (( failures != 0 )); then
    exit 1
fi
