FROM python:3-alpine

RUN pip install flake8

WORKDIR /src
VOLUME ["/src"]

ENTRYPOINT ["flake8"]
