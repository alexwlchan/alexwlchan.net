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
    drafts_dir = "_drafts"

    tracked_drafts = `git ls-tree --name-only HEAD #{drafts_dir}/`.split("\n")

    now = Time.now

    tracked_drafts.each do |entry|
      puts "*** Publishing draft #{entry}"

      name = File.basename(entry)
      new_name = File.join("_posts", now.strftime("%Y"), "#{now.strftime('%Y-%m-%d')}-#{name}")
      FileUtils.mkdir_p File.dirname(new_name)
      File.rename(entry, new_name)

      # Now we write the exact date and time into the top of the file.
      # This means that if I publish more than one post on the same day,
      # they have an unambiguous ordering.
      doc = File.read(new_name)
      doc = doc.gsub(
        /layout:\s+post\s*\n/,
        "layout: post\ndate: #{now}\n")
      File.open(new_name, 'w') { |f| f.write(doc) }

      puts "*** Creating Git commit for #{entry}"
      Shell.execute!("git rm #{entry}")
      Shell.execute!("git add #{new_name}")
      Shell.execute!("git commit -m \"Publish new post #{name}\"")
    end

    FileUtils.rm_rf(drafts_dir)
  end
end


module Jekyll
  module Commands
    class PublishDrafts < Command
      def self.init_with_program(prog)
        prog.command(:"publish-drafts") do |c|
          c.action do |args, options|
            # Hard-coding the source directory here isn't ideal, but I
            # haven't found a way to access the "site" variable inside
            # a Command plugin.
            # TODO: Don't hard-code this bit of configuration!
            publish_all_drafts("src")
          end
        end
      end
    end
  end
end
