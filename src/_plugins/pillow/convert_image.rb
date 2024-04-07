require 'shell/executer'

def convert_image(request)
  unless File.exist? request['out_path']
    request = JSON.generate(request)

    Shell.execute!("$VIRTUAL_ENV/bin/python3 src/_plugins/pillow/convert_image.py #{request}")
  end
end
