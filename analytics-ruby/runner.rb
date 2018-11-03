require "cgi"
require "date"
require "open3"
require "set"
require "uri"


def get_docker_logs(container_name, days)
  stdout, _, _ = Open3.capture3(
    "docker", "logs", "--since", "#{days * 24 * 60}m", container_name)
  stdout.split(/\n/)
end


NGINX_LOG_REGEX = %r{
    ^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s-\s-\s
    \[(?<date>\d{2}\/[A-Z][a-z]{2}\/\d{4}:\d{2}:\d{2}:\d{2}\s(\+|\-)\d{4})\]\s
    "(?:OPTIONS|HEAD|GET|POST)\s(?<url>.+)\sHTTP\/1\.[01]"\s
    (?<status>\d{3})
}x


def parse_lines(lines)
  lines
    .map { |line| NGINX_LOG_REGEX.match(line).named_captures.to_h }
    .each { |h|
      h["status"] = h["status"].to_i
      h["date"] = DateTime.strptime(h["date"], "%d/%b/%Y:%H:%M:%S %z")
    }
end


def get_tracking_data(parsed_lines)
  parsed_lines
    .select { |line| line["url"].start_with?("/analytics/a.gif") }
    .each { |line|
      query_str = line["url"][17..-1]
      parsed_qs = CGI::parse(query_str)
      line["title"] = parsed_qs["t"][0]
      line["referrer"] = parsed_qs["ref"][0]
      line["url"] = parsed_qs["url"][0]
    }
end


def get_interesting_hits
  lines = get_docker_logs("infra_alexwlchan_1", 1)
  parsed_lines = parse_lines(lines)
  get_tracking_data(parsed_lines)
end


def is_generic_search_referrer(ref)
  /^https:\/\/www\.google\.[a-z]+(?:\.[a-z]+)?\/?$/.match(ref) != nil ||
  Set[
    "android-app://com.google.android.googlequicksearchbox/https/www.google.com",
    "https://duckduckgo.com/",
  ].include?(ref) ||
  ref.start_with?("https://www.google.com", "https://www.bing.com/", "http://www.bing.com/")
end


def is_search_traffic(ref)
  is_generic_search_referrer(ref)
end


def extract_query_param(url, query_key)
  CGI::parse(URI.parse(url).query)[query_key][0]
end


def extract_search_referrer(ref)
  if is_generic_search_referrer(ref)
    "[Generic search]"
  elsif ref.start_with?("https://www.google.com", "https://www.bing.com/", "http://www.bing.com/")
    puts extract_query_param(ref, "q")
    extract_query_param(ref, "q")
  else
    ref
  end
end


def summarise_referrers(refs)
  referrers = Hash.new(0)
  refs
    .each { |ref|
      if !is_search_traffic(ref)
        referrers[ref] += 1
      end
    }
  
  referrers
end


def summarise_search_referrers(refs)
  searches = Hash.new(0)
  refs
    .each { |ref|
      if is_search_traffic(ref)
        searches[extract_search_referrer(ref)] += 1
      end
    }

  searches
end

hits = get_interesting_hits()


def get_referrers(hits)
  hits
    .map { |h| h["referrer"] }
    .select { |ref| ref != "" }
    .select { |ref| ! ref.start_with?("https://alexwlchan.net/") }
end

refs = get_referrers(hits)
puts summarise_referrers(refs)
searches = summarise_search_referrers(refs)
puts searches
