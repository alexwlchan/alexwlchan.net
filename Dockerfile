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
COPY src/_plugins/publish_drafts.rb /publish_drafts.rb
RUN mv /publish_drafts.rb /usr/local/bundle/gems/jekyll-$(grep -E 'jekyll \(\d+\.\d+\.\d+\)' Gemfile.lock | awk '{print $2}' | tr -d '()')/lib/jekyll/commands

VOLUME ["/site"]
WORKDIR /site

ENTRYPOINT ["bundle", "exec", "jekyll"]
