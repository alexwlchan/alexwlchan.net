FROM certbot/certbot

RUN apk update && apk add docker
RUN apk add python3 --update-cache --repository http://dl-3.alpinelinux.org/alpine/v3.7/main/

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY renew_certs.py /

ENTRYPOINT ["python3", "/renew_certs.py"]
