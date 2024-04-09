source 'https://rubygems.org'

group :build, optional: true do
  gem 'chunky_png', '~> 1.4'
  gem 'color', '~> 1.8'
  gem 'html-proofer', '~> 5'
  gem 'jekyll', '~> 4'
  gem 'jekyll-include-cache', '~> 0.2'
  gem 'json-schema', '~> 4'
  gem 'nokogiri', '~> 1.16'
  gem 'shell-executer', '~> 1.0'
end

group :lint, optional: true do
  gem 'rubocop', '~> 1.63'

  # These dependencies are specifically for CI in GitHub Actions; I don't
  # need it when I'm running locally.  If I try to run `bundle exec rubocop`
  # in CI without it, I get errors like:
  #
  #     cannot load such file -- rubocop-minitest
  #
  gem 'rubocop-minitest'
  gem 'rubocop-performance'
end

group :test, optional: true do
  gem 'test-unit'
end
