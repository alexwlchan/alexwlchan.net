---
layout: note
title: Create a file atomically in Go
date: 2026-02-22 10:36:29 +00:00
summary: Use `os.CreateTemp` to create a temporary file in the target directory, then do an atomic rename once you've finished writing.
topic: Go
---
Here's an interesting function from the Tailscale repos that [Anton](https://github.com/knyar) told me about in a code review last week: a function to write to a file atomically.
This ensures you don't get partially written data in the final file.

```go {"names":{"1":"WriteFile","2":"filename","3":"data","4":"perm","7":"err","8":"fi","9":"err","20":"f","21":"err","32":"tmpName","42":"err","50":"err","56":"err","61":"err"},"line_numbers":"10-52","caption":"Lines 10–52 of <a href='https://github.com/tailscale/tailscale/blob/8890c3c413d6422c7810719efe4ff3e8c994afa9/atomicfile/atomicfile.go#L10C1-L52'><code>atomicfile/atomicfile.go</code></a> in the <a href='https://github.com/tailscale/tailscale/'>tailscale/tailscale</a> repo. Copyright Tailscale Inc & contributors, used under the BSD-3-Clause license."}
import (
	"fmt"
	"os"
	"path/filepath"
	"runtime"
)

// WriteFile writes data to filename+some suffix, then renames it into filename.
// The perm argument is ignored on Windows, but if the target filename already
// exists then the target file's attributes and ACLs are preserved. If the target
// filename already exists but is not a regular file, WriteFile returns an error.
func WriteFile(filename string, data []byte, perm os.FileMode) (err error) {
	fi, err := os.Stat(filename)
	if err == nil && !fi.Mode().IsRegular() {
		return fmt.Errorf("%s already exists and is not a regular file", filename)
	}
	f, err := os.CreateTemp(filepath.Dir(filename), filepath.Base(filename)+".tmp")
	if err != nil {
		return err
	}
	tmpName := f.Name()
	defer func() {
		if err != nil {
			f.Close()
			os.Remove(tmpName)
		}
	}()
	if _, err := f.Write(data); err != nil {
		return err
	}
	if runtime.GOOS != "windows" {
		if err := f.Chmod(perm); err != nil {
			return err
		}
	}
	if err := f.Sync(); err != nil {
		return err
	}
	if err := f.Close(); err != nil {
		return err
	}
	return Rename(tmpName, filename)
}
```

This is similar to code I've produced in other projects to do atomic file writes -- write to a temporary file first, then do an atomic rename to the final destination.

The temporary file is created in the same directory as the target, to give the best chance of being able to do an atomic rename.
You can't do an atomic rename across filesystem boundaries; using the same directory ensures both files are on the same filesystem.

To handle concurrent writes, I normally insert a random UUID into the temporary filename, so different processes write to different tempfiles.
This is handled automatically by Go's [`os.CreateTemp` function][go-createtemp], which adds a random string to the end of the filename.

The `Rename()` function has different logic for Windows and non-Windows systems:

*   On non-Windows, it uses [`os.Rename()`][go-rename].
    The Go documentation notes that *"even within the same directory, on non-Unix platforms Rename is not an atomic operation"*.
*   On Windows, it makes a syscall to the [`ReplaceFileW` function][ms-replacefilew].
    A cursory Internet search is conflicted on whether this is a truly atomic rename, although concurs that it's the best option on Windows.

[go-createtemp]: https://pkg.go.dev/os#CreateTemp
[go-rename]: https://pkg.go.dev/os#Rename
[ms-replacefilew]: https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew
