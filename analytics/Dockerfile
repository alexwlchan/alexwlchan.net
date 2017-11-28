FROM python:3-alpine

RUN apk update && apk add build-base

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /data
VOLUME ["/data"]

COPY analytics.js /app/analytics.js
COPY analytics.py /app/analytics.py

ENTRYPOINT ["python", "/app/analytics.py"]
