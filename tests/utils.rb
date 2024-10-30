require 'net/http'

def get_url(url)
  uri = URI(url)
  Net::HTTP.get_response(uri)
end
