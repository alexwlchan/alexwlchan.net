# Check that all of my HTTPS certificates are valid and not about
# to expire.

require 'date'
require 'net/http'
require 'test/unit'

# Returns the expiry date of the HTTPS certificate for this domain name
#
# Example:
#
#     > get_cert_expiry("alexwlchan.net")
#     2025-02-14 23:59:59 UTC
#
def get_cert_expiry(hostname)
  uri = URI::HTTPS.build(host: hostname)
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: true)

  cert = response.peer_cert
  cert.not_after
end

# Returns the number of days left before the HTTPS certificate for
# this domain expires
def days_to_expiry(hostname)
  expiry_date = get_cert_expiry(hostname)
  seconds_until = (expiry_date - Time.now).to_i
  seconds_until / (24 * 60 * 60)
end

class TestHttpsCertificateExpiry < Test::Unit::TestCase
  def test_apex
    assert days_to_expiry('alexwlchan.net') > 14
  end

  def test_books
    assert days_to_expiry('books.alexwlchan.net') > 14
  end

  def test_analytics
    assert days_to_expiry('analytics.alexwlchan.net') > 14
  end

  def test_www
    assert days_to_expiry('www.alexwlchan.net') > 14
  end

  def test_dotcom
    assert days_to_expiry('alexwlchan.com') > 14
  end

  def test_www_dotcom
    assert days_to_expiry('www.alexwlchan.com') > 14
  end

  def test_dotcouk
    assert days_to_expiry('alexwlchan.co.uk') > 14
  end

  def test_www_dotcouk
    assert days_to_expiry('www.alexwlchan.co.uk') > 14
  end
end
