FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

# Some links that were useful in getting 'gem install' to work:
#
#   - https://jekyllrb.com/docs/installation/
#   - https://github.com/ffi/ffi/issues/485
#
RUN apk update
RUN apk add build-base libffi-dev ruby ruby-dev ruby-irb ruby-rdoc

RUN gem install bundler jekyll

COPY Gemfile .
COPY Gemfile.lock .
RUN bundle install

WORKDIR /site

ENTRYPOINT ["/usr/bin/jekyll"]
