# not 3.2 because https://github.com/jekyll/jekyll/issues/9233
# https://github.com/jekyll/jekyll/issues/8535
FROM ruby:3.1-slim

LABEL maintainer "Alex Chan <alex@alexwlchan.net>"
LABEL description "Build image for alexwlchan.net"

COPY Gemfile .
COPY Gemfile.lock .

# # This is needed to avoid a segfault/shared library issue when running
# # sassc-ruby inside Alpine.  See https://github.com/sass/sassc-ruby/issues/141
# ENV BUNDLE_FORCE_RUBY_PLATFORM true
#

RUN apt-get update
RUN apt-get install --yes build-essential zlib1g-dev

# https://github.com/mtgrosser/rszr#debian-based
RUN apt-get install --yes libimlib2 libimlib2-dev

RUN apt-get install --yes git
RUN apt-get install --yes rsync
RUN apt-get install --yes exiftool
RUN apt-get install --yes imagemagick

RUN bundle install

#   Dependency Error: Yikes! It looks like you don't have /Users/alexwlchan/repos/alexwlchan.net/src/_plugins/linter.rb or one of its dependencies installed. In order to use Jekyll as currently configured, you'll need to install this gem. If you've run Jekyll with `bundle exec`, ensure that you have included the /Users/alexwlchan/repos/alexwlchan.net/src/_plugins/linter.rb gem in your Gemfile as well. The full error message from Ruby is: 'Could not open library 'libcurl': libcurl: cannot open shared object file: No such file or directory. Could not open library 'libcurl.so': libcurl.so: cannot open shared object file: No such file or directory. Could not open library 'libcurl.so.4': libcurl.so.4: cannot open shared object file: No such file or directory' If you run into trouble, you can find helpful resources at https://jekyllrb.com/help/!

# Package libcurl-dev is a virtual package provided by:
#   libcurl4-openssl-dev 7.74.0-1.3+deb11u3
#   libcurl4-nss-dev 7.74.0-1.3+deb11u3
#   libcurl4-gnutls-dev 7.74.0-1.3+deb11u3
# You should explicitly select one to install.

RUN apt-get install --yes libcurl4-gnutls-dev

# COPY ./scripts/install_jekyll.sh .
# RUN ./install_jekyll.sh
#
ENTRYPOINT ["bundle", "exec", "jekyll"]
