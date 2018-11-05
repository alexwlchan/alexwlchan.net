FROM alpine

RUN apk add --update docker ruby ruby-irb ruby-rdoc
RUN gem install toml-rb

VOLUME ["/analytics"]
WORKDIR /analytics

CMD ["/analytics/runner.rb"]
