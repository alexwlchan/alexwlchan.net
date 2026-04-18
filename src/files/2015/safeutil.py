#!/usr/bin/env python
"""
This is a script designed to be "safe" drop-in replacements for the
shutil move() and copyfile() functions.

These functions are safe because they should never overwrite an
existing file. In particular, if you try to move/copy to dst and
there's already a file at dst, these functions will attempt to copy to
a slightly different (but free) filename, to avoid accidental data loss.

More background here: http://alexwlchan.net/2015/06/safer-file-copying/
"""

import filecmp
import os


def _increment_filename(filename, marker='-'):
    """
    Returns a generator that yields filenames with a counter. This counter
    is placed before the file extension, and incremented with every iteration.

    For example:

        f1 = increment_filename("myimage.jpeg")
        f1.next() # myimage-1.jpeg
        f1.next() # myimage-2.jpeg
        f1.next() # myimage-3.jpeg

    If the filename already contains a counter, then the existing counter is
    incremented on every iteration, rather than starting from 1.

    For example:

        f2 = increment_filename("myfile-3.doc")
        f2.next() # myfile-4.doc
        f2.next() # myfile-5.doc
        f2.next() # myfile-6.doc

    The default marker is an underscore, but you can use any string you like:

        f3 = increment_filename("mymovie.mp4", marker="_")
        f3.next() # mymovie_1.mp4
        f3.next() # mymovie_2.mp4
        f3.next() # mymovie_3.mp4

    Since the generator only increments an integer, it is practically unlimited
    and will never raise a StopIteration exception.
    """
    # First we split the filename into three parts:
    #
    #  1) a "base" - the part before the counter
    #  2) a "counter" - the integer which is incremented
    #  3) an "extension" - the file extension
    basename, fileext = os.path.splitext(filename)

    # Check if there's a counter in the filename already - if not, start a new
    # counter at 0.
    if marker not in basename:
        base = basename
        value = 0

    # If it looks like there might be a counter, then try to coerce it to an
    # integer to get its value. Otherwise, start with a new counter at 0.
    else:
        base, counter = basename.rsplit(marker, 1)

        try:
            value = int(counter)
        except ValueError:
            base = basename
            value = 0

    # The counter is just an integer, so we can increment it indefinitely.
    while True:
        if value == 0:
            value += 1
            yield filename
        value += 1
        yield '%s%s%d%s' % (base, marker, value, fileext)


def copyfile(src, dst):
    """
    Copies a file from path src to path dst.

    If a file already exists at dst, it will not be overwritten, but:

     * If it is the same as the source file, do nothing
     * If it is different to the source file, pick a new name for the copy that
       is distinct and unused, then copy the file there.

    Returns the path to the copy.
    """
    if not os.path.exists(src):
        raise ValueError('Source file does not exist: {}'.format(src))

    # Create a folder for dst if one does not already exist
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    # Keep trying to copy the file until it works
    while True:

        dst_gen = _increment_filename(dst)
        dst = next(dst_gen)

        # Check if there is a file at the destination location
        if os.path.exists(dst):

            # If the namesake is the same as the source file, then we don't
            # need to do anything else.
            if filecmp.cmp(src, dst):
                return dst

        else:

            # If there is no file at the destination, then we attempt to write
            # to it. There is a risk of a race condition here: if a file
            # suddenly pops into existence after the `if os.path.exists()`
            # check, then writing to it risks overwriting this new file.
            #
            # We write by transferring bytes using os.open(). Using the O_EXCL
            # flag on the dst file descriptor will cause an OSError to be
            # raised if the file pops into existence; the O_EXLOCK stops
            # anybody else writing to the dst file while we're using it.
            try:
                src_fd = os.open(src, os.O_RDONLY)
                dst_fd = os.open(dst,
                                 os.O_WRONLY|os.O_EXCL|os.O_CREAT|os.O_EXLOCK)

                # Read 100 bytes at a time, and copy them from src to dst
                while True:
                    data = os.read(src_fd, 100)
                    os.write(dst_fd, data)

                    # When there are no more bytes to read from the source
                    # file, 'data' will be an empty string
                    if not data:
                        break

                # If we get to this point, then the write has succeeded
                return dst

            # An OSError errno 17 is what happens if a file pops into existence
            # at dst, so we print an error and try to copy to a new location.
            # Any other exception is unexpected and should be raised as normal.
            except OSError as e:
                if e.errno != 17 or e.strerror != 'File exists':
                    raise
                else:
                    print('Race condition: %s just popped into existence' % dst)

            finally:
                os.close(src_fd)
                os.close(dst_fd)

        # Copying to this destination path has been unsuccessful, so increment
        # the path and try again
        dst = next(dst_gen)


def move(src, dst):
    """
    Moves a file from path src to path dst.

    If a file already exists at dst, it will not be overwritten, but:

     * If it is the same as the source file, do nothing
     * If it is different to the source file, pick a new name for the copy that
       is distinct and unused, then copy the file there.

    Returns the path to the new file.
    """
    dst = copyfile(src, dst)
    os.remove(src)
    return dst
