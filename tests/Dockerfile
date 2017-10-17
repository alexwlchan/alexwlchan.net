FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Image for running tests of the alexwlchan.net build"

RUN apk update && apk add git python py-pip py2-lxml

RUN pip install -e git+https://github.com/rubys/feedvalidator#egg=src&subdirectory=src

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /tests

CMD ["py.test"]
