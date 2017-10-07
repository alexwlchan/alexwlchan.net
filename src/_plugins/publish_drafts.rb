# This command does some automation with the _drafts folder.  Specifically,
# when run, it:
#
#  * Copies every file from _drafts into _posts, into my preferred folder
#    structure (one folder per year)
#  * Creates a Git commit for the change
#  * Pushes said Git commit to GitHub
#
# It gets copied directly into the Docker container, rather than being
# installed as a gem, because installing local gems adds a whole extra layer
# of complication that I don't want right now.

require 'fileutils'
require 'shell/executer.rb'


def publish_all_drafts(source_dir)
  Dir.chdir(source_dir) do
    drafts_dir = File.join(source_dir, "_drafts")
    if not Dir.exist? drafts_dir
      return
    end

    now = Time.now

    Dir.glob("#{drafts_dir}/*.md") do |entry|
      puts "*** Publishing draft #{entry}"

      now = Time.now

      name = File.basename(entry)
      new_name = File.join(source_dir, "_posts", now.strftime("%Y"), "#{now.strftime('%Y-%m-%d')}-#{name}")
      File.rename(name, new_name)

      puts "*** Creating Git commit for #{entry}"
      Shell.execute!("git rm #{drafts_dir}/#{entry}")
      Shell.execute!("git add #{new_name}")
      Shell.execute!("git commit -m \"[auto] Publish draft entry #{entry}\"")
    end

    FileUtils.rm_rf(drafts_dir)
  end
end


module Jekyll
  module Commands
    class PublishDrafts < Command
      def self.init_with_program(prog)
        prog.command(:"publish-drafts") do |c|

          c.option 'source', '-s', '--source SOURCE', 'Custom source directory'

          c.action do |args, options|
            publish_all_drafts(options['source'])
          end
        end
      end
    end
  end
end
