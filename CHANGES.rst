=================
Changes for pypsh
=================

Unreleased
==========

2015-07-13: 0.7.3
=================

 - detect hosts from Host entries in `~/.ssh/config`

 - fixed support for ``--pty``

2014-05-01: 0.7.2
=================

 - fixed matching of hosts that have a custom port configured.

 - added the `--pty` option.

 - stdout or stderr buffers filling up should no longer cause pypsh to get stuck

2014-03-14: 0.7.1
=================

 - **bugfix**: adopt paramiko missing_host_key usage to changed API

2014-03-14: 0.7.0
=================

 - **breaking change**
   Changed the commandline interface again. The `hostregex` is now always the
   first (required) parameter. In addition the `cmd` subcommand is now again
   optional and pypsh also supports to execute commands that are read from
   stdin.

   So the following invokations are possible::

    pypsh "myhosts[0-9]" "uptime"
    echo "uptime" | pypsh "myhosts[0-9]"
    pypsh "myhosts[0-9]" cmd "uptime"
    pypsh "myhosts[0-9]" copy /tmp/source /tmp/destination

   The `wait` and `serial` parameters have been merged into `interval`
   If the interval is zero the commands will be executed in parallel, if it's
   greater than zero the command/copy process will be serial with a sleep of
   `interval` after each host.

   In addition, the `show` subcommand has been removed. Simply use `uptime` or
   some other harmless command to show which hosts matched.

2013-06-24: 0.6.0
=================

 - **feature**: added new `--wait` parameter to the `cmd` subcommand.

2013-06-24: 0.5.0
=================

 - **feature**: added new `show` subcommand.

2013-05-16: 0.4.0
=================

 - **feature**: added new `copy` subcommand. Therefore the `cmd` command has
   to be specified explicitly and is no longer the default command.

2013-03-28: 0.3.0
=================

 - **feature**: added --serial (-s) parameter to run commands serial instead of
   parallel.

2013-03-01: 0.2.0
=================

 - **feature**: output is now colored

 - **feature**: a summary of matched hosts is printed before cmd execution

 - **feature**: a summary of (un)successful cmd invokations is printed after cmd
   execution

 - **bugfix**: improved error handling in case of wrong regex or ssh connection
   errors.

 - **bugfix**: fixed erroneous import in setup.py that caused it to require all
   dependencies to be already installed.

2013-02-12: 0.1.0
=================

 - initial version
