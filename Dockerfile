# Note: I can't use Ruby 3.2 yet because Jekyll uses Liquid 4, and Liquid 4
# throws an exception if you use it with Ruby 3.2:
#
#     Liquid Exception: undefined method `tainted?' for { ... post ...}
#
# The fix is available in Liquid 5, but that isn't supported by Jekyll yet.
#
# There are various bugs tracking this on the Jekyll repository, e.g. see
# https://github.com/jekyll/jekyll/issues/9233
# https://github.com/jekyll/jekyll/issues/8535
#
# If/when Jekyll allows a Liquid upgrade, then I can bump this to Ruby 3.2.
FROM ruby:3.1-slim

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

COPY ./scripts/install_imagemagick7.sh .
RUN ./install_imagemagick7.sh

COPY Gemfile .
COPY Gemfile.lock .

COPY ./scripts/install_jekyll.sh .
RUN ./install_jekyll.sh

ENTRYPOINT ["bundle", "exec", "jekyll"]
