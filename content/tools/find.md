---
author: Shailesh Kumar
title: The good old find tool
date: 2025-09-22
weight: 1
tags: 
  - Tool
  - Command Line
category: Programming
---

We are inundated with hundreds of new tools every day.
Often, it is easy to forget about the time-tested tools that can still do wonders.
The good old `find` is one such
tool sitting idle on your computers (Linux, Mac OS, and Windows).
Effort into mastering `find` can pay significant dividends—saving time,
reducing manual errors, and unleashing new workflows.

Whether you’re a seasoned sysadmin or a curious newcomer, reinvesting a bit of
effort into mastering `find` can pay significant dividends—saving time,
reducing manual errors, and unleashing new workflows. In a world filled with
ever-complex solutions, sometimes the simplest tools are those that stand the
test of time.

## Key Strengths of `find`

* **Diverse Search Criteria**: You can search for files by name, type, size,
  modification time, ownership (user or group), permissions, and more. This makes
  it far more potent than simple wildcard searches. For example, you can find all
  files larger than 10MB that were modified in the last 24 hours.
* **Recursive Searching**: `find` traverses a directory tree, searching all
  subdirectories by default. This is one of its core functions and makes it ideal
  for locating a file when you only know its general location, like a home
  directory or a project folder.
* **Actionable Results**: Beyond just listing files, `find` can execute commands
  on the files it locates. This is typically done with the `-exec` option. For
  instance, you could find all `.log` files older than 7 days and delete them
  with a single command.
* **Efficiency**: `find` is a very efficient tool for large directory structures
  because it performs the search directly on the filesystem's metadata, not by
  reading file contents. This makes it very fast, especially when searching for
  attributes like modification time or size.
* **Fine-grained Control**: The tool offers a high degree of control over the
  search process, including options to limit the depth of the search, follow
  symbolic links, or invert the search criteria to find files that *don't* match
  a specific pattern.

In this post, we will rediscover the remarkable versatility and effectiveness of the
`find` tool. We will begin by exploring its core strengths and why it remains
relevant for searching and managing files in any environment. Next, we will break
down practical examples that cover common scenarios, from simple searches to more
advanced operations, such as filtering by time, size, or permissions, and even
automating actions across your file system.

## Basic Usage

Find a file by name in the current directory

```shell
find . -name "filename.txt"
```

Ignore case while searching

```shell
find . -iname "filename.txt"
```

Find all directories

```shell
find . -type d
```

Find all files

```shell
find . -type f
```

Find all symbolic links

```shell
find . -type l
```

All files that are not directories

```shell
find . -not -type d
```

All empty files and directories

```shell
find . -empty
```

Limit search depth

```shell
find . -maxdepth 2 -name "*.conf"
```

## Working with Directories

Find all directories named `node_modules`

```shell
find . -type d -name "node_modules"
```

Find directories that contain files with `.js` extension

```shell
find . -type f -name "*.js" -print0 | xargs -0 -I {} dirname {} | sort -u
```

Let's break this down:

* `find .`: Start the search from the current directory (`.`)
* `-type f`: Only consider files (not directories, symlinks, etc.).
* `-name "*.js"`: Look for files ending with `.js`. The `*` is a wildcard for any characters.
* `-print0`: Prints the full file path, terminated by a null character. This is safer than `-print` when dealing with filenames that might contain spaces or special characters.
* `| xargs -0 -I {} dirname {}`:
  * `|`: Pipes the output of `find` to `xargs`.
  * `xargs -0`: Reads null-separated input from the pipe.
  * `-I {} dirname {}`: For each null-separated filename, execute the `dirname` command, replacing `{}` with the filename. `dirname` extracts the directory path from a full file path.
* `| sort -u`:
  * `|`: Pipes the output of `dirname` to `sort`.
  * `sort -u`: Sorts the list of directory paths and removes duplicates (since multiple `.js` files in the same directory would list that directory numerous times).

### Empty Directories

Finding empty directories

```shell
find . -type d -empty
```

* `.`: Specifies the starting point of the search. A dot `.` means the current directory. You can replace it with any other path, like `/home/user/documents`.
* `-type d`: Restricts the search to only directories.
* `-empty`: A condition that matches empty files or directories.
The command will output a list of all empty directories within the specified path.

Removing empty directories:

```shell
find . -type d -empty -delete
```

This command finds all empty directories in the current path and immediately deletes them. The `-delete` option is applied after the `-empty` condition is met.

Alternative

```shell
find . -type d -empty -print0 | xargs -0 rmdir
```

* `find ... -print0`: This prints the found directories, with each name ending in a null character `\0`. This is the safest way to handle filenames that might contain spaces or special characters.
* `xargs -0`: This command takes the null-delimited input from `find` and passes it as arguments to the `rmdir` command.
* `rmdir`: This command removes empty directories. It will fail if a directory is not empty, which adds a layer of safety.

## Working with Files

### Basic Search

Find files matching a regular expression

```shell
find . -regex '.*\.html'
```

Find a file and its directory path

```shell
find . -name "report.pdf" -printf "%h\n"
```

### File Size

Find files larger than a specific size:

```shell
find . -size +10M # Mega bytes
find . -size +1G # Giga bytes
find . -size +10c # bytes
find . -size +10k # kilo bytes
```

Find files of an exact size:

```shell
find . -size 512c # Exact 512 bytes
```

Files of size within a range:

```shell
find . -size +5k -size -10M # between 5K to 10MB
```

Files that are not empty

```shell
find . -not -empty -type f
```

### Timestamps (Accessed/Modified)

Files modified in last 24 hours:

```shell
find . -mtime -1 #1 day old or less
```

Files accessed more than 7 days ago

```shell
find . -atime +7 #+ means more, 7 days
```

Find files modified in a specific time range:

```shell
find . -mtime +1 -mtime -3 # between 1 to 3 days ago
```

### Ownership

Files owned by a specific user

```shell
find . -user username
```

Files not owned by a specific user:

```shell
find . -not -user username
```

Belonging to a specific group:

```shell
find . -group groupname
```

### Permissions

Files with a specific permission mode:

```shell
find . -perm 755
```

Files with at least a specific permission mode:

```shell
find . -perm -644
```

Change permissions on all HTML files

```shell
find . -name "*.html" -exec chmod 644 {} \;
```

Find files with permissions that are not readable by the owner:

```shell
find . -perm /u-r
```

The `/` prefix with `-perm` means to find any file that does **not** have the specified permission. This example finds files where the user does not have read permissions.

### File Extensions

Find files matching an extension (up to a search depth)

```shell
find . -maxdepth 2 -name "*.conf"
```

Find files with multiple extensions

```shell
find . -name "*.jpg" -o -name "*.png"
```

The `-o` (OR) operator finds files that match either of the two names. You must enclose the entire expression in parentheses and escape them `\(` and `\)` or quote them to avoid shell interpretation.

```shell
find . \( -name "*.jpg" -o -name "*.png" \)
```

### Links (Hard/Soft)

Find files with more than 2 hard links:

```shell
find . -links +2
```

### INode

Find files with a specific inode number:

```shell
find . -inum 12345
```

### Metadata

Find files whose metadata (ownership or permissions) was changed in the last one hour:

```shell
find . -cmin -60
```

### Deletion

Delete all temporary files

```shell
find . -name "*.tmp" -delete
```

## More Actions

### Zip

Find and zip log files

```shell
find . -name "*.log" -exec zip logs.zip {} +
```

### Copy

Copying files to another directory

```shell
find . -name "*.bak" -exec cp {} /tmp/backups/ \;
```

This finds all files ending in `.bak` and copies them to the `/tmp/backups/` directory.

### Move

Find and move all mp3 files to a different directory:

```shell
find . -name "*.mp3" -exec mv {} /media/music/ \;
```

### LS

Find and list files with their sizes and permissions:

```shell
find . -type f -print0 | xargs -0 ls -lh
```

### WC

Find and count the number of files with a specific extension:

```shell
find . -name "*.jpg" | wc -l
```

### Search inside Files

Run grep on found files

```shell
find . -name "*.log" -exec grep "ERROR" {} +
```

Using `+` at the end instead of `\;` is more efficient because it passes multiple file paths to a single instance of the command, rather than executing it once per file.

## Mac OS Specific

Finding `.DS_Store` files

```shell
find . -name ".DS_Store"
```

Deleting them

```shell
find . -name ".DS_Store" -delete
```

Alternative

```shell
find . -name ".DS_Store" -print0 | xargs -0 rm
```

## Epilogue

Throughout this post, we explored the enduring power and flexibility of the `find` tool. We looked at its key strengths, including its ability to filter files and directories using a wide range of criteria, perform recursive searches, and take automated actions on results. We covered practical use cases—from basic searches and advanced filtering to working with file attributes, permissions, and timestamps—as well as typical maintenance tasks like deleting or archiving files. Altogether, we’ve seen how `find` remains an essential command-line tool that can save time, streamline workflows, and enhance your overall productivity no matter your experience level.
