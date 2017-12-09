FROM python:3-alpine

RUN apk update && apk add docker

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY reports.py /

ENTRYPOINT ["python3", "/reports.py"]
