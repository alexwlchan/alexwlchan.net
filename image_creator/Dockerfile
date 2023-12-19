FROM alpine

RUN apk add imagemagick \
            imagemagick-jpeg \
            ruby
RUN gem install shell-executer

COPY ./create_images.rb /create_images.rb

ENTRYPOINT ["/create_images.rb"]
