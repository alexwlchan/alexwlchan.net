---
layout: post
date: 2024-05-25 13:21:10 +00:00
title: Documenting my DNS records
summary: |
  Exporting my DNS records as YAML gives me a plaintext file where I can track changes, add comments, and feel more confident about managing my DNS.
tags:
  - dns
  - blogging about blogging
  - ruby
colors:
  index_light: "#c53f70"
  index_dark:  "#bbc660"
---
{% comment %}
    Card photo from https://www.pexels.com/photo/close-up-shot-of-a-hummingbird-4838540/
{% endcomment %}

I had to change some of my DNS records recently, a phrase which strikes fear into the heart of sysadmins everywhere.
It all went fine, but I definitely felt like I was playing with fire.

My current domain registrar is [Hover], and the only way I can manage my domains is through a web dashboard on their website:

{%
  picture
  filename="dns_dashboard.png"
  width="739"
  alt="Screenshot of a web dashboard. There's a table of records, one record per row, and an edit button on the right-hand side."
  class="screenshot"
%}

It's easy to make a one-off change in this dashboard, but it's harder to manage a set of DNS records over a long period.
There are two big things it's missing:

*   No documentation – there's nowhere to keep notes or comments, so I can't write down why I created a particular record or if I still need it.

*   No edit history – changes are immediate, and overwrite whatever was there before.
    If I break something, there's no button to rollback or revert -- I'm expected to just know what the old, working configuration was, and apply that as new.

One way to get both of these would be to use an infrastructure-as-code (IaC) tool to manage my DNS records, which is how I've managed DNS records at multiple jobs.
I could define my DNS records in code, add inline comments, and track changes in Git.

Unfortunately there are no IaC tools for Hover -- it doesn't even have a public API -- so that approach is out.
(If I was starting from scratch, one of the reasons I'd pick a different domain registrar is so I could use a proper IaC tool.)
I could migrate my domains to another service, but that's a big change and I'm a bit nervous doing that without any sort of safety net.

However, I've still found a way to add documentation and change history to my existing setup.
This adds a safety net that makes me feel more comfortable making changes, and opens the door to me moving my domains elsewhere.

[Hover]: https://www.hover.com





## Getting a snapshot of my existing DNS records

This project started when I learnt about Alex Dalitz's gem [dnsruby], which lets you list DNS records in Ruby.
Here's a simple example:

```ruby
require 'dnsruby'  # dnsruby (1.72.1)

dns = Dnsruby::DNS.new
records = dns.getresources('alexwlchan.net', 'TXT')

puts records.map(&:rdata_to_string)
# "v=spf1 include:spf.messagingengine.com ?all"
# "ahrefs-site-verification_c8470a858a715b78845c1b81e2dc2f7aa8b367ced4cd8d342a3986a33a03b84c"
# "google-site-verification=o3zoiEGC6aLEgPMKiyWHZcRZrutF6wHQjKqhkRvgWiQ"
```

You have to know exactly which domain name and record type you want to query -- I don't think there's an easy way to get all the DNS records for a particular domain, especially if you want to include all the subdomains.
This is a limitation of DNS, not the dnsruby gem.

But that's not an issue for me, because I know what subdomains and record types I'm using -- I can read them out of my web dashboard.
By iterating over the possible domains and record types, I wrote a script that gets all my DNS records and saves them to a YAML file:

```ruby
require 'date'
require 'yaml'

require 'dnsruby'

def get_dns_records(domain, record_type)
  dns = Dnsruby::DNS.new
  records = dns.getresources(domain, record_type)
  records.map(&:rdata_to_string).sort
end

domains_to_check = {
  'alexwlchan.net'        => ['NS', 'MX', 'A', 'TXT'],
  'books.alexwlchan.net'  => ['CNAME'],
  'social.alexwlchan.net' => ['CNAME'],
  # ...and several other domains and subdomains
}

dns_records =
  domains_to_check
    .flat_map do |domain, record_types|
      record_types.map do |rt|
        [domain, rt, get_dns_records(domain, rt)]
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
```

Here's a little snippet of the YAML it produces:

```
---
alexwlchan.net NS:
- ns1.hover.com.
- ns2.hover.com.
alexwlchan.net MX:
- 20 in2-smtp.messagingengine.com.
- 10 in1-smtp.messagingengine.com.
alexwlchan.net A:
- 75.2.60.5
…
```

This is already an improvement on what I had before -- if I run this script on a schedule, I'll have snapshots of what my DNS looked like on a particular date.
I could use that to construct an edit history, and it would make it easier for me to revert a bad change.
If I make a change and break something, I can look at a previous snapshot to see what working configuration I should re-apply.

And now I have my DNS records in a plaintext file, I can add comments.

[dnsruby]: https://github.com/alexdalitz/dnsruby





## Adding documentation to my DNS snapshots

I started rearranging one of these YAML snapshots, grouping similar records from different domains and adding comments to explain what they're for.
For example, I can add a comment to remind me where the IP address `75.2.60.5` comes from:

```
# == Netlify DNS records ==
#
# These are DNS records that allow me to use my own domains with my sites
# hosted on Netlify.
#
# See https://docs.netlify.com/domains-https/custom-domains/configure-external-dns/

alexwlchan.net A:   [ "75.2.60.5", ]
alexwlchan.com A:   [ "75.2.60.5", ]
alexwlchan.co.uk A: [ "75.2.60.5", ]
```

I went through the snapshot and added a comment for every DNS record -- now I know why created each record.
It took a while, but now I have a much better understanding of what my DNS is doing, and what's safe to change in the future.
You can read the [fully-commented file](https://github.com/alexwlchan/alexwlchan.net/blob/e30e26d135b6e94cc28a040543910be37a25019f/dns/dns_records.yml) on GitHub.
This file is now the canonical statement of what my DNS records should be.

I wrote a second script that can compare two YAML snapshots: do my live DNS records match this canonical statement?

```ruby
require 'yaml'

expected_records = YAML.load_file(ARGV[0])
actual_records   = YAML.load_file(ARGV[1])

if expected_records == actual_records
  puts 'The DNS records match 🥳'
  exit 0
else
  puts "The DNS records don't match! 😱"

  (expected_records.keys + actual_records.keys).uniq.each do |k|
    next unless expected_records[k] != actual_records[k]

    puts "#{k}:"
    puts " - expected: #{expected_records[k].inspect}"
    puts " - actual:   #{actual_records[k].inspect}"
  end

  exit 1
end
```

Here's the output:

```console
$ ruby compare_dns_records.rb dns_records.yml dns_records.good.yml
The DNS records match 🥳

$ ruby compare_dns_records.rb dns_records.yml dns_records.bad.yml
The DNS records don't match! 😱
alexwlchan.net A:
 - expected: ["75.2.60.5"]
 - actual:   ["57.2.60.5"]
```

In the first case, all my DNS records are configured correctly.
In the second case, I've typo'd `75` as `57` -- now I know that I need to go and fix something in my Hover dashboard.

It can't actually fix the mistake, only tell me that something's wrong -- but this is much better than what I had before.





## An infrastructure-as-code future

I'm going to leave my DNS records in Hover for now, but these scripts have also give me ideas for how I might migrate out of Hover, if I ever decide to do so.
One of the tricky parts is replicating all my existing DNS records in a new service -- how do I know I've done that correctly?

Fortunately, dnsruby is very flexible.
Currently the nameserver for `alexwlchan.net` is at Hover, and their nameserver is `ns1.hover.com`.
When you do a DNS lookup for my domain, it asks `ns1.hover.com` for the DNS records.

But I can tell dnsruby to ignore that, and to ask Linode's nameserver instead:

```ruby
require 'dnsruby'

dns = Dnsruby::DNS.new({:nameserver => ["ns1.linode.com"]})
records = dns.getresources('alexwlchan.net', 'TXT')
puts records.map(&:rdata_to_string).inspect
# []
```

I feel like this could give me more reassurance when I copy DNS records between providers.
First, I copy my existing DNS records into the new provider.
Then, I use dnsruby to get snapshots of the DNS records being served by my old/new provider's nameservers.
Finally, I compare the two snapshots to check they match.

Crucially, I could do this *before I switch the domain to the new provider's nameservers*.
This gives me time to test, to iterate, to fix silly mistakes, and I can do so at a relaxed pace without worrying if my site/email are down.





## Conclusion

You can see the complete code [on GitHub](https://github.com/alexwlchan/alexwlchan.net/tree/main/dns).

These two scripts allow me to do regular checks of my DNS.
I have them set to run as a daily job in GitHub Actions.
First, I create a snapshot of my live DNS records.
Then, I compare those records to the canonical statement of what I expect my DNS to be.
If the two have diverged, the job will fail and I'll get an alert, and I'll go to investigate.

I can also run the check on demand, if I'm actively making changes.

This doesn't change anything in Hover or the way I manage my DNS records, but it's done wonders for my peace of mind.
I now have some written documentation about all of my DNS records are for, and I have an edit history so I can easily revert any breaking changes.

