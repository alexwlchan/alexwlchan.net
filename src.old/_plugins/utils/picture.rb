# frozen_string_literal: true

# Generates a map (path) -> (colour profile)
def get_colour_profiles(dirname)
  # Flags:
  #
  #    -r = recursive, search for every file in the folder
  #    -quiet -quiet = ignore warnings
  #
  exiftool_output = `exiftool -r -quiet -quiet -printFormat '$directory/$filename : $profileDescription' #{dirname}/** 2>&1`

  # There are two possible outputs for the line, of the form:
  #
  #     src/_tests/images/gradient-with-p3.png : Display P3
  #
  #     Warning: [Minor] Tag 'profileDescription' not defined - src/_tests/images/gradient-with-srgb.png
  #
  exiftool_output
    .split("\n")
    .to_h do |line|
      if line.start_with?("Warning: [Minor] Tag 'profileDescription' not defined - ")
        path = line.split(' - ')[-1]
        path = path.strip

        [path, nil]
      else
        path, profile = line.split(':')
        path = path.strip!
        profile = profile.strip!

        [path, profile]
      end
    end
end
