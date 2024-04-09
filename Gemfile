source 'https://rubygems.org'

group :build do
  gem 'chunky_png', '~> 1.4'
  gem 'color', '~> 1.8'
  gem 'html-proofer', '~> 5'
  gem 'jekyll', '~> 4'
  gem 'jekyll-include-cache', '~> 0.2'
  gem 'json-schema', '~> 4'
  gem 'nokogiri', '~> 1.16'
  gem 'shell-executer', '~> 1.0'
end

group :lint do
  gem 'rubocop', '~> 1.63'

  # This dependency is specifically for CI in GitHub Actions; I don't
  # need it when I'm running locally.  If I try to run `bundle exec rubocop`
  # in CI without it, I get an error:
  #
  #     cannot load such file -- rubocop-minitest
  #
  gem 'rubocop-minitest', '~> 0.35.0'
end
