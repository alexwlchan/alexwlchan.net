FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

RUN apk update && \
    apk add ruby && \
    gem install --no-document bundler

ENTRYPOINT ["bundler"]
