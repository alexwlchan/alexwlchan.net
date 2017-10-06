require 'jekyll-compose'
require 'shell/executer.rb'

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

def publish_all_drafts(source_dir, git_commit, git_push)
  Dir.chdir(source_dir) do
    drafts_dir = File.join(source_dir, "_drafts")
    if not Dir.exist? drafts_dir
      return
    end

    now = Time.now
    has_changes = false

    Dir.glob("#{drafts_dir}/*.md") do |entry|
      puts "*** Publishing draft #{entry}"
      new_file = Jekyll::Commands::NewPublish.process(
        args = [entry],
        options = {'source': source_dir, 'date': now}
      )

      if git_commit
        puts "*** Creating Git commit for #{entry}"
        Shell.execute!("git rm #{entry}")
        Shell.execute!("git add #{File.join(source_dir, new_file)}")
        Shell.execute!("git commit -m \"[auto] Publish draft entry #{entry}\"")
        has_changes = true
      end
    end

    if git_push and has_changes
      puts "*** Pushing new commits to GitHub"
      Shell.execute!("git push origin")
    end
  end
end

module Jekyll
  module Commands
    class PublishDrafts < Command
      def self.init_with_program(prog)
        prog.command(:"publish-drafts") do |c|

          c.option 'source', '-s', '--source SOURCE', 'Custom source directory'
          c.option 'commit', '--commit', 'Create corresponding Git commits'
          c.option 'push', '--push', 'Push the commits to GitHub'

          c.action do |args, options|
            publish_all_drafts(
              source = options['source'],
              git_commit = options['commit'],
              git_push = options['push']
            )
          end
        end
      end
    end

    # Subclasses based on jekyll-compose.  The two relevant changes:
    #
    #  * Posts are sorted into per-year directories, because that's the
    #    folder structure I prefer
    #  * process() returns the path to the new file, so I can pass it to
    #    `git add`.
    #

    class NewPublish < Commands::Publish
      def self.process(args = [], options = {})
        params = PublishArgParser.new args, options
        params.validate!

        movement = NewDraftMovementInfo.new params

        mover = DraftMover.new movement, params.source
        mover.move
        movement.to
      end
    end

    class NewDraftMovementInfo < Commands::DraftMovementInfo
      def to
        date_stamp = params.date.strftime '%Y-%m-%d'
        year = params.date.strftime "%Y"
        "_posts/#{year}/#{date_stamp}-#{params.name}"
      end
    end
  end
end
