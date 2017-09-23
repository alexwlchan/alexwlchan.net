FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Image for running tests of the alexwlchan.net build"

RUN apk update
RUN apk add git python python3
RUN pip3 install tox

# lxml dependencies
RUN apk add build-base libxml2-dev libxslt-dev python3-dev

WORKDIR /tests

ENTRYPOINT ["tox"]
