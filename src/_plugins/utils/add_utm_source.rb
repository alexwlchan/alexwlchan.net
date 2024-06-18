# frozen_string_literal: true

require 'uri'

# Add a `utm_source` parameter to a URL.
#
# For now this will always be "alexwlchan".  This is to make it easier
# for external sites to see that I'm sending them traffic.
#
def add_utm_source(url)
  u = URI.parse(url)
  new_query = URI.decode_www_form(u.query || '') << %w[utm_source alexwlchan]
  u.query = URI.encode_www_form(new_query)
  u.to_s
end
