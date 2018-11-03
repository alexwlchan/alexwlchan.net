FROM alpine

RUN apk add --update docker ruby

VOLUME ["/analytics"]
WORKDIR /analytics

CMD ["/analytics/runner.rb"]
