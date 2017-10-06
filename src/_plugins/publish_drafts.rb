# This command does some automation with the _drafts folder.  Specifically,
# when run, it:
#
#  * Copies every file from _drafts into _posts, into my preferred folder
#    structure (one folder per year)
#  * Adds the current date to the YAML front matter
#  * Creates a Git commit for the change
#  * Pushes said Git commit to GitHub
#
# It gets copied directly into the Docker container, rather than being
# installed as a gem, because installing local gems adds a whole extra layer
# of complication that I don't want right now.

def publish_all_drafts(drafts_dir: "_drafts")
  if not Dir.exist? drafts_dir
    return
  end

  Dir.glob("#{drafts_dir}/*.md") do |entry|
    puts entry
  end
end

module Jekyll
  module Commands
    class PublishDrafts < Command
      class << self
        def init_with_program(prog)
          prog.command(:"publish-drafts") do |c|

            c.option 'source', '-s', '--source SOURCE', 'Custom source directory'

            c.action do |args, options|
              publish_all_drafts()
            end
          end
        end
      end
    end
  end
end
