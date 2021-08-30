#!/usr/bin/env ruby

require "yaml"

ELSEWHERE_YML_PATH = "src/_data/elsewhere.yml"

elsewhere = YAML.load_file(ELSEWHERE_YML_PATH)

File.open(ELSEWHERE_YML_PATH, "w") { |f| f.write(elsewhere.to_yaml) }

puts elsewhere