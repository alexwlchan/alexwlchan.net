#!/usr/bin/env python3
"""
Usage:

    sudo python3 ignore_folders_in_spotlight.py [PATH]

This script will tell Spotlight to ignore any folder in/under PATH
that's named "node_modules" or "target".

If PATH is omitted, it uses the current working directory.

Written by Alex Chan.
See https://alexwlchan.net/2021/08/ignore-lots-of-folders-in-spotlight/

"""

import datetime
import os
import subprocess
import sys
import xml.etree.ElementTree as ET


# The list of directory names that should be ignored
IGNORE_DIRECTORIES = {"node_modules", "target"}

# Path to the Spotlight plist on Catalina
SPOTLIGHT_PLIST_PATH = "/System/Volumes/Data/.Spotlight-V100/VolumeConfiguration.plist"


def get_dir_paths_under(root):
    """
    Generates the paths of every directory under ``root``.
    """
    for dirpath, dirnames, _ in os.walk(root):
        for name in dirnames:
            yield os.path.abspath(os.path.join(root, dirpath, name))


def create_backup_of_spotlight_plist():
    """
    Save a backup of the Spotlight configuration to the Desktop before
    we start.

    This gives us a way to rollback, and also is a nondestructive check
    that we have the right permissions to modify the Spotlight config.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d.%H-%M-%S")
    backup_path = os.path.join(
        os.environ["HOME"], "Desktop", f"Spotlight-V100.VolumeConfiguration.{now}.plist"
    )

    try:
        subprocess.check_call(["cp", SPOTLIGHT_PLIST_PATH, backup_path])
    except subprocess.CalledProcessError as err:
        print(f"*** Could not create backup of Spotlight configuration", file=sys.stderr)
        print(f"*** You need to run this script with 'sudo'", file=sys.stderr)
        sys.exit(1)

    print( "*** Created backup of Spotlight configuration",             file=sys.stderr)
    print( "*** If this script goes wrong or you want to revert, run:", file=sys.stderr)
    print( "***",                                                       file=sys.stderr)
    print(f"***     sudo cp {backup_path} {SPOTLIGHT_PLIST_PATH}",     file=sys.stderr)
    print( "***     sudo launchctl stop com.apple.metadata.mds",        file=sys.stderr)
    print ("***     sudo launchctl start com.apple.metadata.mds",       file=sys.stderr)
    print( "***",                                                       file=sys.stderr)


def get_paths_to_ignore(root):
    """
    Generates a list of paths to ignore in Spotlight.
    """
    for path in get_dir_paths_under(root):
        if os.path.basename(path) in IGNORE_DIRECTORIES:

            # Check this path isn't going to be ignored by a parent path.
            #
            # e.g. consider the path
            #
            #       ./dotorg/node_modules/koa/node_modules
            #
            # We're also going to ignore the path
            #
            #       ./dotorg/node_modules
            #
            # so adding an ignore for this deeper path is unnecessary.
            relative_parts = os.path.relpath(path, root).split("/")
            this_name = relative_parts.pop(-1)

            if any(parent_dir in IGNORE_DIRECTORIES for parent_dir in relative_parts):
                continue

            yield path


def get_current_ignores():
    """
    Returns a list of paths currently ignored by Spotlight.
    """
    output = subprocess.check_output([
        "plutil",

        # Get the value of the "Exclusions" key as XML
        "-extract", "Exclusions", "xml1",

        # Send the result to stdout
        "-o", "-",

        SPOTLIGHT_PLIST_PATH
    ])

    # The result of this call will look something like:
    #
    #
    #     <?xml version="1.0" encoding="UTF-8"?>
    #     <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    #     <plist version="1.0">
    #     	<array>
    #     		<string>/Users/alexwlchan/repos/pipeline/target</string>
    #     		<string>/Users/alexwlchan/repos/pipeline/node_modules</string>
    #     	</array>
    #     </plist>
    #
    return {s.text for s in ET.fromstring(output).iter("string")}


def ignore_path_in_spotlight(path):
    """
    Ignore a path in Spotlight, if it's not already ignored.
    """
    already_ignored = get_current_ignores()

    if path in already_ignored:
        return

    subprocess.check_call([
        "plutil",

        # Insert at the end of the Exclusions list
        "-insert", f"Exclusions.{len(already_ignored)}",

        # The path to exclude
        "-string", os.path.abspath(path),

        # Path to the Spotlight plist on Catalina
        SPOTLIGHT_PLIST_PATH
    ])


if __name__ == '__main__':
    try:
        root = sys.argv[1]
    except IndexError:
        root = "."

    create_backup_of_spotlight_plist()

    print("*** The following paths will be ignored by Spotlight")
    for path in get_paths_to_ignore(root=root):
        ignore_path_in_spotlight(path)
        print(path)

    subprocess.check_call("launchctl stop com.apple.metadata.mds", shell=True)
    subprocess.check_call("launchctl start com.apple.metadata.mds", shell=True)
