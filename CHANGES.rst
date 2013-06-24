=================
Changes for pypsh
=================

Unreleased
==========

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
