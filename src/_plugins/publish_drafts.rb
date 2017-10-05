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

module Jekyll
  module Commands
    class PublishDrafts < Command
      class << self
        def init_with_program(prog)
          prog.command(:"publish-drafts") do |c|
            c.action do |args, options|
              Jekyll.logger.info "Hello!"
            end
          end
        end
      end
    end
  end
end
