FROM alpine

RUN apk update && \
    apk add certbot python3

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY renew_certs.py /

CMD ["/renew_certs.py"]
