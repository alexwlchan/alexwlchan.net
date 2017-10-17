FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Image for running tests of the alexwlchan.net build"

RUN apk update && apk add git python py-pip py2-lxml

# TODO: It's frustrating that this is supplied here, rather than in the
# requirements.txt; it's a bug in the version of pip-tools I use.
RUN pip install -e git+https://github.com/rubys/feedvalidator#egg=src&subdirectory=src

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /tests

CMD ["py.test"]
