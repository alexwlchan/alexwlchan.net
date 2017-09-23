FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Image for running tests of the alexwlchan.net build"

RUN apk update
RUN apk add git libxml2-dev python python3
RUN pip3 install tox

WORKDIR /tests

ENTRYPOINT ["tox"]
