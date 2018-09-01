FROM python:3-alpine

RUN apk update && apk add docker

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

VOLUME ["/app"]
WORKDIR /app

ENTRYPOINT ["python3", "/app/reports.py"]
