# Parse the params string, which is designed to be written with
# a similar syntax to HTML attributes, e.g.
#
#     {% picture filename="IMG_5744.jpg" alt="A black steam engine" %}
#
def parse_attrs(input)
  result = {}

  input.scan(/(?<key>[a-z\-_]+)(?:="(?<value>[^"]*)")?/).each do |k, v|
    result[k] = v
  end

  result
end

# Extract an attribute and remove it from the list.
#
#     > @attrs = { :color => "red", :sides => 5 }
#     => {:color=>"red", :sides=>5}
#
#     > get_required_attribute(@attrs, { :tag => "shape", :attribute => :sides })
#     => 5
#
#     > @attrs
#     => {:color=>"red"}
#
# This is equivalent to calling `dict.pop()` in Python.
#
def get_required_attribute(attrs, opts)
  result = attrs.delete(opts[:attribute])

  raise SyntaxError, "Error in `#{opts[:tag]}` tag: missing required `#{opts[:attribute]}` attribute" if result.nil?

  result
end
