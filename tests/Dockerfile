FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Image for running tests of the alexwlchan.net build"

RUN apk add --update ca-certificates git libxslt-dev python py-pip py2-lxml wget unzip

# TODO: It's frustrating that this is supplied here, rather than in the
# requirements.txt; it's a bug in the version of pip-tools/pip I use.
RUN wget https://github.com/rubys/feedvalidator/archive/master.zip && \
    unzip master.zip >/dev/null && \
    cd feedvalidator-master/src && \
    python setup.py install

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /repo/tests

CMD ["py.test"]
