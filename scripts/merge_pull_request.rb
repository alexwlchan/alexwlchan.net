#!/usr/bin/env ruby

require 'net/http'
require 'json'
require 'uri'

# GITHUB_REF is the tag ref that triggered the workflow run,
# which for pull requests looks something like 'refs/pull/496/merge'.
GITHUB_REF = ENV['GITHUB_REF']

GITHUB_TOKEN = ENV['GITHUB_TOKEN']
REPO = 'alexwlchan/alexwlchan.net'
BASE_URL = "https://api.github.com/repos/#{REPO}"
HEADERS = {
  'Accept' => 'application/vnd.github.v3+json',
  'Authorization' => "token #{GITHUB_TOKEN}",
  'X-GitHub-Api-Version' => '2022-11-28'
}

def api_request(method, url)
  uri = URI.join("#{BASE_URL}/", url.gsub(%r{^/}, ''))
  req = case method
        when :get then Net::HTTP::Get.new(uri)
        when :put then Net::HTTP::Put.new(uri)
        when :delete then Net::HTTP::Delete.new(uri)
        end
  HEADERS.each { |key, value| req[key] = value }
  response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) { |http| http.request(req) }
  JSON.parse(response.body) if response.body && !response.body.empty?
end

def current_merge_commit
  `git rev-parse HEAD`.strip
end

def other_checks_are_running(branch_name)
  checks_resp = api_request(:get, "/commits/#{branch_name}/check-runs")

  if checks_resp['check_runs'].nil?
    abort "!!! check-runs API returned an unexpected response: #{checks_resp}"
  end

  checks = checks_resp['check_runs'].reject { |cr| cr['name'] == 'Merge pull request' }

  checks.each do |cr|
    if cr['status'] == 'completed' && cr['conclusion'] != 'success'
      abort "!!! Check run '#{cr['name']}' did not succeed"
    end
  end

  checks.any? { |cr| cr['status'] != 'completed' }
end

if !GITHUB_REF.start_with?('refs/pull/')
  abort "GITHUB_REF=#{GITHUB_REF}; is this a pull request?"
end

pr_number = GITHUB_REF.split('/')[2]
puts "Deduced pull request as https://github.com/#{REPO}/pull/#{pr_number}"

# Get information about the pull request, in particular the name
# of the branch.
#
# See https://docs.github.com/en/rest/pulls/pulls#get-a-pull-request
pr_resp = api_request(:get, "/pulls/#{pr_number}")
branch_name = pr_resp['head']['ref']
puts "This PR is coming from branch #{branch_name}"

if pr_resp['draft']
  puts 'This is a draft PR, so not merging'
  exit 0
end

sleep 20
sleep(1) while other_checks_are_running(branch_name)

# Check if the branch has been updated since this build started;
# if so, the build on the newer commit takes precedent.
merge_commit_id = pr_resp['merge_commit_sha']
puts "The current merge commit on the branch is '#{merge_commit_id}'"

if merge_commit_id != current_merge_commit
  puts "The current merge commit in GitHub is #{current_merge_commit}; not the same as this build; aborting"
  exit 0
end

# Now look for other checks and see if they succeeded.
#
# See https://docs.github.com/en/rest/checks/runs?apiVersion=2022-11-28#list-check-runs-for-a-git-reference
checks_resp = api_request(:get, "/commits/#{branch_name}/check-runs")
succeeded_checks = checks_resp['check_runs'].each_with_object([]) do |cr, acc|
  next if cr['name'] == 'Merge pull request'

  if cr['status'] != 'completed'
    abort "!!! Check run '#{cr['name']}' has not completed"
  end

  if cr['conclusion'] != 'success'
    abort "!!! Check run '#{cr['name']}' did not succeed"
  end

  acc << cr['name']
end

if succeeded_checks.empty?
  puts 'No other check runs triggered, okay to merge'
else
  puts "All other check runs succeeded, okay to merge (#{succeeded_checks.join(', ')})"
end

api_request(:put, "/pulls/#{pr_number}/merge")
api_request(:delete, "/git/refs/heads/#{branch_name}")
