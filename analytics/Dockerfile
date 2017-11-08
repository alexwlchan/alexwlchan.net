FROM python:3-alpine

COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /data
VOLUME ["/data"]

COPY reports.py /app

ENTRYPOINT ["/app/reports.py"]
