FROM alexwlchan/bundler-base

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

COPY install_specktre.sh .
RUN ./install_specktre.sh

COPY Gemfile .
COPY Gemfile.lock .

COPY install_jekyll.sh .
RUN ./install_jekyll.sh

WORKDIR /site

ENTRYPOINT ["bundle", "exec", "jekyll"]
