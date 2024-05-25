#!/usr/bin/env ruby
# Create a YAML file with a snapshot of my DNS records.
#
# The YAML file will be a list of key-value pairs, where the key is
# the domain name and record type, and the value is a list of records.
#
# The script will print the name of the newly-created YAML file, which
# will include the date the DNS records were retrieved.
#
# == Example output ==
#
# Here is some example YAML output:
#
#     alexwlchan.net NS: ["ns1.hover.com.", "ns2.hover.com."]
#     alexwlchan.net MX: ["10 in1-smtp.messagingengine.com."]
#
# This represents three records for the domain ``alexwlchan.net``:
#
# *   Two NS record with the values ``ns1.hover.com.`` and ``ns2.hover.com.``
# *   One MX record with the value ``in1-smtp.messagingengine.com.`` and priority ``10``
#

require 'date'
require 'yaml'

require 'dnsruby'

domains_to_check = {
  #
  # alexwlchan.net
  'alexwlchan.net' => %w[NS MX A TXT],
  # '_acme-.alexwlchan.net' => %w[TXT],
  'analytics.alexwlchan.net' => %w[A],
  'books.alexwlchan.net' => ['CNAME'],
  'social.alexwlchan.net' => ['CNAME'],
  'til.alexwlchan.net' => ['CNAME'],
  'www.alexwlchan.net' => ['CNAME'],
  'fm1._domainkey.alexwlchan.net' => ['CNAME'],
  'fm2._domainkey.alexwlchan.net' => ['CNAME'],
  'fm3._domainkey.alexwlchan.net' => ['CNAME'],
  '_dmarc.alexwlchan.net' => ['TXT'],

  # alexwlchan.com
  'alexwlchan.com' => %w[NS A MX],
  '*.alexwlchan.com' => ['A'],
  'mail.alexwlchan.com' => ['CNAME'],

  # alexwlchan.co.uk
  'alexwlchan.co.uk' => %w[NS A MX],
  '*.alexwlchan.co.uk' => ['A'],
  'mail.alexwlchan.co.uk' => ['CNAME'],

  # finduntaggedtumblrposts.com
  'finduntaggedtumblrposts.com' => %w[NS A MX TXT],
  'fm1._domainkey.finduntaggedtumblrposts.com' => ['CNAME'],
  'fm2._domainkey.finduntaggedtumblrposts.com' => ['CNAME'],
  'fm3._domainkey.finduntaggedtumblrposts.com' => ['CNAME'],

  # bijouopera.co.uk
  'bijouopera.co.uk' => %w[NS MX A TXT],
  'fm1._domainkey.bijouopera.co.uk' => ['CNAME'],
  'fm2._domainkey.bijouopera.co.uk' => ['CNAME'],
  'fm3._domainkey.bijouopera.co.uk' => ['CNAME']
}

dns_records = Dnsruby::DNS.open do |dns|
  domains_to_check
    .flat_map do |domain, record_types|
      record_types.map do |rt|
        resources = dns.getresources(domain, rt).map(&:rdata_to_string).sort
        [domain, rt, resources]
      end
    end
end

now = DateTime.now.strftime('%Y-%m-%d.%H-%M-%S')
File.write(
  "dns_records.#{now}.yml",
  dns_records
    .to_h { |domain, rt, resources| ["#{domain} #{rt}", resources] }
    .to_yaml
)

puts "dns_records.#{now}.yml"
