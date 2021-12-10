Bash Journey
=================

.. contents:: Table of contents
    :backlinks: top

Disk usage per directory
------------------------

.. code-block:: console
    
    $ du -hs */
    52K     dist/
    5.5M    docs/
    417K    htmlcov/
    124K    src/
    25K     tests/

To sort the output pipe the result to the ``sort`` command:

.. code-block:: console

    $ du -hs */ | sort -hr
    5.5M    docs/
    417K    htmlcov/
    124K    src/
    52K     dist/
    25K     tests/

Disk usage (``du``) command related help:

.. code-block:: none

    Usage: du [OPTION]... [FILE]...
    or:  du [OPTION]... --files0-from=F
    Summarize disk usage of the set of FILEs, recursively for directories.

    Mandatory arguments to long options are mandatory for short options too.
    ...
    -h, --human-readable  print sizes in human readable format (e.g., 1K 234M 2G)
    ...
    -s, --summarize       display only a total for each argument
    ...

Disk usage (``du``) command full help:

.. code-block:: none

    Usage: du [OPTION]... [FILE]...
    or:  du [OPTION]... --files0-from=F
    Summarize disk usage of the set of FILEs, recursively for directories.

    Mandatory arguments to long options are mandatory for short options too.
    -0, --null            end each output line with NUL, not newline
    -a, --all             write counts for all files, not just directories
        --apparent-size   print apparent sizes, rather than disk usage; although
                            the apparent size is usually smaller, it may be
                            larger due to holes in ('sparse') files, internal
                            fragmentation, indirect blocks, and the like
    -B, --block-size=SIZE  scale sizes by SIZE before printing them; e.g.,
                            '-BM' prints sizes in units of 1,048,576 bytes;
                            see SIZE format below
    -b, --bytes           equivalent to '--apparent-size --block-size=1'
    -c, --total           produce a grand total
    -D, --dereference-args  dereference only symlinks that are listed on the
                            command line
    -d, --max-depth=N     print the total for a directory (or file, with --all)
                            only if it is N or fewer levels below the command
                            line argument;  --max-depth=0 is the same as
                            --summarize
        --files0-from=F   summarize disk usage of the
                            NUL-terminated file names specified in file F;
                            if F is -, then read names from standard input
    -H                    equivalent to --dereference-args (-D)
    -h, --human-readable  print sizes in human readable format (e.g., 1K 234M 2G)
        --inodes          list inode usage information instead of block usage
    -k                    like --block-size=1K
    -L, --dereference     dereference all symbolic links
    -l, --count-links     count sizes many times if hard linked
    -m                    like --block-size=1M
    -P, --no-dereference  don't follow any symbolic links (this is the default)
    -S, --separate-dirs   for directories do not include size of subdirectories
        --si              like -h, but use powers of 1000 not 1024
    -s, --summarize       display only a total for each argument
    -t, --threshold=SIZE  exclude entries smaller than SIZE if positive,
                            or entries greater than SIZE if negative
        --time            show time of the last modification of any file in the
                            directory, or any of its subdirectories
        --time=WORD       show time as WORD instead of modification time:
                            atime, access, use, ctime or status
        --time-style=STYLE  show times using STYLE, which can be:
                                full-iso, long-iso, iso, or +FORMAT;
                                FORMAT is interpreted like in 'date'
    -X, --exclude-from=FILE  exclude files that match any pattern in FILE
        --exclude=PATTERN    exclude files that match PATTERN
    -x, --one-file-system    skip directories on different file systems
        --help     display this help and exit
        --version  output version information and exit

    Display values are in units of the first available SIZE from --block-size,
    and the DU_BLOCK_SIZE, BLOCK_SIZE and BLOCKSIZE environment variables.
    Otherwise, units default to 1024 bytes (or 512 if POSIXLY_CORRECT is set).

    The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
    Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).
    Binary prefixes can be used, too: KiB=K, MiB=M, and so on.

    GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
    Full documentation <https://www.gnu.org/software/coreutils/du>
    or available locally via: info '(coreutils) du invocation'


Execute command multiple times with ``xargs``
---------------------------------------------

Let's start with simple example. We want to create directories named ``test-one``, 
``test-two`` and ``test-three``. We can do it by running the ``mkdir`` command multiple times:

.. code-block:: console

    $ mkdir test-one
    $ mkdir test-two
    $ mkdir test-three

You could achieve the same by using the ``xargs`` command:

.. code-block:: console

    $ echo $'test-one\ntest-two\ntest-three' | xargs mkdir

The ``echo`` command prints three lines to the output::

    test-one
    test-two
    test-three    

The output is sent (piped) to the ``xargs`` command's standard input. For each line from the
input the ``xargs`` command executes the specified ``mkdir`` command, passing the content of 
the line as to ``mkdir``. 

This has the same effect as running the ``mkdir`` command three times as we did eariler.

To clean up we could do the same, but this time we use the ``rm`` command to remove the directories
we created.

.. code-block:: console

    echo $'test-one\ntest-two\ntest-three' | xargs rm -r

``xargs`` has a lot of options which could be used to modify it's behavior. Here are just some of them:

.. code-block:: console

    $ echo -n 'one two three' | xargs -I % -t -d ' '  echo say %
    echo say one 
    say one
    echo say two
    say two
    echo say three
    say three

- ``-I %`` option changes the argument placeholder to ``%``
- ``-t`` option instructs xargs to print the command before executing
- ``-d ' '`` option changes the argument separator from the standard input
- ``echo say %`` is the command which ``xargs`` will execute for each argument 
  from the input. ``%`` denotes a placeholder where ``xargs`` places the actual
  argument value.

Here is the full output of the ``xargs`` help:

.. code-block:: none

    Usage: ls [OPTION]... [FILE]...
    List information about the FILEs (the current directory by default).
    Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

    Mandatory arguments to long options are mandatory for short options too.
    -a, --all                  do not ignore entries starting with .
    -A, --almost-all           do not list implied . and ..
        --author               with -l, print the author of each file
    -b, --escape               print C-style escapes for nongraphic characters
        --block-size=SIZE      with -l, scale sizes by SIZE when printing them;
                                e.g., '--block-size=M'; see SIZE format below
    -B, --ignore-backups       do not list implied entries ending with ~
    -c                         with -lt: sort by, and show, ctime (time of last
                                modification of file status information);
                                with -l: show ctime and sort by name;
                                otherwise: sort by ctime, newest first
    -C                         list entries by columns
        --color[=WHEN]         colorize the output; WHEN can be 'always' (default
                                if omitted), 'auto', or 'never'; more info below
    -d, --directory            list directories themselves, not their contents
    -D, --dired                generate output designed for Emacs' dired mode
    -f                         do not sort, enable -aU, disable -ls --color
    -F, --classify             append indicator (one of */=>@|) to entries
        --file-type            likewise, except do not append '*'
        --format=WORD          across -x, commas -m, horizontal -x, long -l,
                                single-column -1, verbose -l, vertical -C
        --full-time            like -l --time-style=full-iso
    -g                         like -l, but do not list owner
        --group-directories-first
                                group directories before files;
                                can be augmented with a --sort option, but any
                                use of --sort=none (-U) disables grouping
    -G, --no-group             in a long listing, don't print group names
    -h, --human-readable       with -l and -s, print sizes like 1K 234M 2G etc.
        --si                   likewise, but use powers of 1000 not 1024
    -H, --dereference-command-line
                                follow symbolic links listed on the command line
        --dereference-command-line-symlink-to-dir
                                follow each command line symbolic link
                                that points to a directory
        --hide=PATTERN         do not list implied entries matching shell PATTERN
                                (overridden by -a or -A)
        --hyperlink[=WHEN]     hyperlink file names; WHEN can be 'always'
                                (default if omitted), 'auto', or 'never'
        --indicator-style=WORD  append indicator with style WORD to entry names:
                                none (default), slash (-p),
                                file-type (--file-type), classify (-F)
    -i, --inode                print the index number of each file
    -I, --ignore=PATTERN       do not list implied entries matching shell PATTERN
    -k, --kibibytes            default to 1024-byte blocks for disk usage;
                                used only with -s and per directory totals
    -l                         use a long listing format
    -L, --dereference          when showing file information for a symbolic
                                link, show information for the file the link
                                references rather than for the link itself
    -m                         fill width with a comma separated list of entries
    -n, --numeric-uid-gid      like -l, but list numeric user and group IDs
    -N, --literal              print entry names without quoting
    -o                         like -l, but do not list group information
    -p, --indicator-style=slash
                                append / indicator to directories
    -q, --hide-control-chars   print ? instead of nongraphic characters
        --show-control-chars   show nongraphic characters as-is (the default,
                                unless program is 'ls' and output is a terminal)
    -Q, --quote-name           enclose entry names in double quotes
        --quoting-style=WORD   use quoting style WORD for entry names:
                                literal, locale, shell, shell-always,
                                shell-escape, shell-escape-always, c, escape
                                (overrides QUOTING_STYLE environment variable)
    -r, --reverse              reverse order while sorting
    -R, --recursive            list subdirectories recursively
    -s, --size                 print the allocated size of each file, in blocks
    -S                         sort by file size, largest first
        --sort=WORD            sort by WORD instead of name: none (-U), size (-S),
                                time (-t), version (-v), extension (-X)
        --time=WORD            with -l, show time as WORD instead of default
                                modification time: atime or access or use (-u);
                                ctime or status (-c); also use specified time
                                as sort key if --sort=time (newest first)
        --time-style=TIME_STYLE  time/date format with -l; see TIME_STYLE below
    -t                         sort by modification time, newest first
    -T, --tabsize=COLS         assume tab stops at each COLS instead of 8
    -u                         with -lt: sort by, and show, access time;
                                with -l: show access time and sort by name;
                                otherwise: sort by access time, newest first
    -U                         do not sort; list entries in directory order
    -v                         natural sort of (version) numbers within text
    -w, --width=COLS           set output width to COLS.  0 means no limit
    -x                         list entries by lines instead of by columns
    -X                         sort alphabetically by entry extension
    -Z, --context              print any security context of each file
    -1                         list one file per line.  Avoid '\n' with -q or -b
        --append-exe           append .exe if cygwin magic was needed
        --help     display this help and exit
        --version  output version information and exit

    The SIZE argument is an integer and optional unit (example: 10K is 10*1024).
    Units are K,M,G,T,P,E,Z,Y (powers of 1024) or KB,MB,... (powers of 1000).
    Binary prefixes can be used, too: KiB=K, MiB=M, and so on.

    The TIME_STYLE argument can be full-iso, long-iso, iso, locale, or +FORMAT.
    FORMAT is interpreted like in date(1).  If FORMAT is FORMAT1<newline>FORMAT2,
    then FORMAT1 applies to non-recent files and FORMAT2 to recent files.
    TIME_STYLE prefixed with 'posix-' takes effect only outside the POSIX locale.
    Also the TIME_STYLE environment variable sets the default style to use.

    Using color to distinguish file types is disabled both by default and
    with --color=never.  With --color=auto, ls emits color codes only when
    standard output is connected to a terminal.  The LS_COLORS environment
    variable can change the settings.  Use the dircolors command to set it.

    Exit status:
    0  if OK,
    1  if minor problems (e.g., cannot access subdirectory),
    2  if serious trouble (e.g., cannot access command-line argument).

    GNU coreutils online help: <https://www.gnu.org/software/coreutils/>
    Full documentation <https://www.gnu.org/software/coreutils/ls>
    or available locally via: info '(coreutils) ls invocation'

Here are some typical uses of the ``xargs`` command:

.. code-block:: console

    $ # Remove files older than two weeks
    $ find /tmp -mtime +14 | xargs rm
    $ # Same but using the find's -exec option. Notice the \; at the end
    $ find /tmp -mtime +14 -exec rm {} \;
    $ # Prompt before executing the each command
    $ find /tmp -mtime +14 | xargs -p rm


.. seealso::

    - `12 Practical Examples of Linux Xargs Command for Beginners <https://www.tecmint.com/xargs-command-examples/>`_

