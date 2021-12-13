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

    Usage: xargs [OPTION]... COMMAND [INITIAL-ARGS]...
    Run COMMAND with arguments INITIAL-ARGS and more arguments read from input.

    Mandatory and optional arguments to long options are also
    mandatory or optional for the corresponding short option.
    -0, --null                   items are separated by a null, not whitespace;
                                    disables quote and backslash processing and
                                    logical EOF processing
    -a, --arg-file=FILE          read arguments from FILE, not standard input
    -d, --delimiter=CHARACTER    items in input stream are separated by CHARACTER,
                                    not by whitespace; disables quote and backslash
                                    processing and logical EOF processing
    -E END                       set logical EOF string; if END occurs as a line
                                    of input, the rest of the input is ignored
                                    (ignored if -0 or -d was specified)
    -e, --eof[=END]              equivalent to -E END if END is specified;
                                    otherwise, there is no end-of-file string
    -I R                         same as --replace=R
    -i, --replace[=R]            replace R in INITIAL-ARGS with names read
                                    from standard input; if R is unspecified,
                                    assume {}
    -L, --max-lines=MAX-LINES    use at most MAX-LINES non-blank input lines per
                                    command line
    -l[MAX-LINES]                similar to -L but defaults to at most one non-
                                    blank input line if MAX-LINES is not specified
    -n, --max-args=MAX-ARGS      use at most MAX-ARGS arguments per command line
    -o, --open-tty               Reopen stdin as /dev/tty in the child process
                                    before executing the command; useful to run an
                                    interactive application.
    -P, --max-procs=MAX-PROCS    run at most MAX-PROCS processes at a time
    -p, --interactive            prompt before running commands
        --process-slot-var=VAR   set environment variable VAR in child processes
    -r, --no-run-if-empty        if there are no arguments, then do not run COMMAND;
                                    if this option is not given, COMMAND will be
                                    run at least once
    -s, --max-chars=MAX-CHARS    limit length of command line to MAX-CHARS
        --show-limits            show limits on command-line length
    -t, --verbose                print commands before executing them
    -x, --exit                   exit if the size (see -s) is exceeded
        --help                   display this help and exit
        --version                output version information and exit

    Please see also the documentation at http://www.gnu.org/software/findutils/.
    You can report (and track progress on fixing) bugs in the "xargs"
    program via the GNU findutils bug-reporting page at
    https://savannah.gnu.org/bugs/?group=findutils or, if
    you have no web access, by sending email to <bug-findutils@gnu.org>.

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

