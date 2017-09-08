FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

COPY Gemfile .
COPY Gemfile.lock .

COPY install_jekyll.sh .
RUN ./install_jekyll.sh

WORKDIR /site

ENTRYPOINT ["/usr/bin/jekyll"]
