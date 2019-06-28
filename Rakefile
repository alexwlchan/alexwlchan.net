require "jekyll"

task :build do
  Jekyll::Commands::Build.process({:lint => true})
end

task :serve do |args, options|
  Jekyll::Commands::Serve.start({
    "host" => "0.0.0.0",
    "port" => 5757,
    "watch" => true,
    "show_drafts" => true,
    "incremental" => true,
    "livereload_port" => 35729,
    "serving" => true,
  })
end

task :'publish-drafts' do
  $LOAD_PATH.unshift File.expand_path("src/_plugins", __dir__)
  require "publish_drafts"

  Jekyll::Commands::PublishDrafts.process()
end
