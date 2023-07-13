FROM alpine

RUN apk add imagemagick ruby
RUN gem install shell-executer

COPY ./create_images.rb /create_images.rb

ENTRYPOINT ["/create_images.rb"]
