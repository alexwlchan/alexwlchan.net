require 'nokogiri'

html_doc = Nokogiri::HTML("<html><body><p>Hello world</p></body></html>")
puts html_doc
