#!/usr/bin/env ruby
# Compare two YAML files created by ``save_dns_records_as_yaml.rb``
#
# This script takes two arguments: each a path to a YAML file that
# describes some DNS records.  The script then compares the records:
#
#   - If the DNS records are the same, it exits with code 0
#   - If the DNS records differ, it exits with code 1
#

require 'yaml'

unless ARGV.length == 2
  warn "Usage: #{$PROGRAM_NAME} EXPECTED_RECORDS_YAML ACTUAL_RECORDS_YAML"
  exit 1
end

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
