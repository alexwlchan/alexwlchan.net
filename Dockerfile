FROM ruby:2.4-alpine3.6

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

COPY install_specktre.sh .
RUN ./install_specktre.sh

COPY Gemfile .
COPY Gemfile.lock .

COPY install_jekyll.sh .
RUN ./install_jekyll.sh

# This is copied directly into the file to save me the hassle of installing
# it from a Gem.
COPY src/_plugins/publish_drafts.rb /usr/local/bundle/gems/jekyll-3.6.0/lib/jekyll/commands

WORKDIR /site

ENTRYPOINT ["bundle", "exec", "jekyll"]
