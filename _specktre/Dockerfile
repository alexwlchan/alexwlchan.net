FROM alpine

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build Specktre assets for alexwlchan.net"

RUN apk update
RUN apk add build-base jpeg-dev python3 python3-dev zlib-dev && \
    pip3 install Pillow && \
    apk del build-base python3-dev

RUN apk add git optipng

RUN pip3 install specktre==0.2.0

COPY . /specktre

WORKDIR /site

CMD ["python3", "/specktre/build_banners.py"]
