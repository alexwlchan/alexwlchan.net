"""The cURL command line tool allows you to specify multiple URLs in a single
string. For example:
 
    http://site.{one,two,three}.com
    ftp://ftp.numericals.com/file[1-100].txt
    ftp://ftp.numericals.com/file[001-100].txt (with leading zeros)
    ftp://ftp.letters.com/file[a-z].txt
 
This module can take a string in this format, and return the list of strings
that it specifies. The exact syntax can be seen in the examples on the cURL man
page [1]. It's rough around the edges, but should work fine with correctly 
formatted strings.
 
To invoke, use the parse_string function on a string:
 
    >>> urls = curlparser.parse_string("http://site.{one,two,three}.com")
    >>> urls.next()
    "http://site.one.com"
    >>> urls.next()
    "http://site.two.com"
    >>> urls.next()
    "http://site.three.com"
 
    >>> files = curlparser.parse_string("ftp://ftp.nums.com/file[1-100].txt")
    >>> files.next()
    "ftp://ftp.nums.com/file1.txt"
    ...
    >>> files.next()
    "ftp://ftp.nums.com/file99.txt"
    >>> files.next()
    "ftp://ftp.nums.com/file100.txt"
 
or supply the string as a command-line argument (wrap in quotes to avoid the
string being mangled by the shell):
 
    $ python curlparser.py "http://www.letters.com/file[a-z:2].txt"
    http://www.letters.com/filea.txt
    http://www.letters.com/filec.txt
    http://www.letters.com/filee.txt
    ...
    http://www.letters.com/filew.txt
    http://www.letters.com/filey.txt
 
For other notes, see the associated blog post. [2]
 
Created by Alex Chan (alexwlchan.net) in November 2014.
 
[1]: http://curl.haxx.se/docs/manpage.html
[2]: http://alexwlchan.net/2014/11/ranged-strings/
"""
 
import itertools
import re
 
# These regexes match the different set/range operators. They have () as they
# need to capture the content when we split the string.
 
ITEMISED_SET    = re.compile(r"({[a-zA-Z0-9,]{1,}})")
LOWERCASE_RANGE = re.compile(r"(\[[a-z]{1}\-[a-z]{1}(?::[0-9-]{1})?\])")
UPPERCASE_RANGE = re.compile(r"(\[[A-Z]{1}\-[A-Z]{1}(?::[0-9-]{1})?\])")
NUMERIC_RANGE   = re.compile(r"(\[[0-9]{1,}\-[0-9]{1,}(?::-?[0-9]{1,})?\])")
 
# Utility functions
 
def flatten(alist):
    return list(itertools.chain(*alist))
 
def sign(number):
    """Returns the sign of a given number."""
    if number != 0:
        return number / abs(number)
    else:
        return 0
 
# Parser functions
 
def tokenize_string(astr):
    """Break a string down into a list of tokens. A token is a set, a range or
    a set of characters that gives a unique string. Examples:
    
    "http://www.site{1,2,3}.com" ~> ["http://www.site", "{1,2,3}", ".com"]
    "easy as {a,b,c} or [1-3]"   ~> ["easy as ", "{a,b,c}", " or ", "[1-3]"]
    """
    tokens = [astr]
    for regex in [ITEMISED_SET, LOWERCASE_RANGE,
        UPPERCASE_RANGE, NUMERIC_RANGE]:
        tokens = flatten(map(lambda s: re.split(regex, s), tokens))
    return tokens
 
def parse_token(token):
    """Given a single 'token' element, return a list of values that the token
    expands to. For example:
    
    {1,2,3}   ~> [1, 2, 3]
    [1-10]    ~> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    [17-5:-3] ~> [17, 14, 11, 8, 5]
    [a-z:5]   ~> [a, f, k, p, u, z]
    abc       ~> [abc]
    
    All entries in the returned list are strings. Single strings are returned 
    as a singleton.
    """
    if ITEMISED_SET.match(token):
        return token[1:-1].split(',')
    
    elif LOWERCASE_RANGE.match(token) or UPPERCASE_RANGE.match(token) or \
        NUMERIC_RANGE.match(token):
        
        # Get the step from the range, or default to 1.
        if ':' in token:
            step = int(token[1:-1].split(':')[-1])
        else:
            step = 1
        token = token[1:-1].split(':')[0]
        start, end = token.split('-')
        
        # Capture the length of the string so we can include leading zeros.
        l_zeros = len(start)
        
        # Python ranges are half-open, whereas the given ranges are always
        # closed at both ends. We take the sign of the step to determine how to
        # adjust the range, because the range may be descending.
        if start.isdigit():
            start = int(start)
            end   = int(end) + sign(step)
            return map(lambda s: str(s).zfill(l_zeros), range(start, end, step))
        else:
            return map(chr, range(ord(start), ord(end) + sign(step), step))
            
    # If it doesn't match one of the previous expressions, then the token is a
    # plain string.
    else:
        return [token]
 
def parse_string(astr):
    """Take a string formatted in cURL syntax and return a list of strings 
    which it expands to.
    """
    token_lists = map(parse_token, tokenize_string(astr))
    return itertools.imap(lambda p: ''.join(p), itertools.product(*token_lists))
    
def main():
    """Print a list of strings that arise from a single cURL format string."""
    import sys
    print '\n'.join(list(parse_string(sys.argv[1])))
 
if __name__ == '__main__':
    main()