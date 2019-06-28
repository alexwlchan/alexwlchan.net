require "jekyll"

task :build do
  Jekyll::Commands::Build.process({:lint => true})
end

task :serve do
  Jekyll::Commands::Serve.process({})
end

task :'publish-drafts' do
  $LOAD_PATH.unshift File.expand_path("src/_plugins", __dir__)
  require "publish_drafts"
  Jekyll::Commands::PublishDrafts.process()
end
