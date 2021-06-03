require "html-proofer"


class RunLinting < Jekyll::Command
  class << self
    def init_with_program(prog)
      prog.command(:lint) do |cmd|
        cmd.action do |_, options|
          options = configuration_from_options(options)
          run_linting(options["destination"])
        end
      end
    end

    def run_linting(dirname)
      HTMLProofer.check_directory(
        dirname, opts = {
          :check_html => false,
          :check_img_http => true,
          :disable_external => true,
          :empty_alt_ignore => true,
          :report_invalid_tags => true,
        }).run
    end
  end
end
