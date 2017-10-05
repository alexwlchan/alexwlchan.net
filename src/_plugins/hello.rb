module Jekyll
  module Commands
    class Hello < Command
      class << self
        def init_with_program(prog)
          prog.command(:hello) do |c|
            c.action do |args, options|
              Jekyll.logger.info "Hello!"
            end
          end
        end
      end
    end
  end
end
