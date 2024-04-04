# frozen_string_literal: true

# Convert a tweet avatar into a base64-encoded string.
#
# Avatars are routinely quite large (e.g. 512x512), but they're
# only displayed in a 36x36 square (see _tweets.scss).
#
# Cutting a smaller thumbnail should reduce the page weight.
#
def get_tweet_avatar(path)
  cache = Jekyll::Cache.new('TweetAvatars')

  last_mtime = File.mtime(path)

  cache.getset("#{path} :: #{last_mtime}") do
    `.venv/bin/python3 src/_plugins/utils/get_tweet_avatar.py #{Shellwords.escape(path)}`
  end
end
