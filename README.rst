
=======================
Parallel SSH with Regex
=======================

Why `pypsh` instead of dsh?
===========================

Because managing group files with dsh is tedious. Pypsh requires no
configuration, it just works.

Similar to dsh, pypsh can be used to execute a command on multiple hosts in
parallel. In addition it is also possible to copy a file to multiple hosts at
once. See below for further usage instructions.

The command or file copy operation will be executed on any host that is in the
`known_hosts` file and matches the given regular expression.

This means in order for pypsh to know about a host it is necessary to connect
to it at least once with plain ssh.

Command Execution
=================

To execute a command on a group of hosts matching a given regular expression::

    pypsh cmd <hostregex> <cmd-to-execute>

E.g.::

    pypsh cmd "role\d+\.customer\.your\.domain" "uptime"

Instead of executing the commands in parallel it is also possible to execute
the commands one after another. To do so use::

    pypsh cmd -s "role\d+\.customer\.your\.domain" "uptime"

Or to wait between the commands (which might be useful when restarting services
like elasticsearch that are part of a cluster)::

    pypsh cmd -w 60 "role\d+\.customer\.your\.domain" "uptime"

List matching hosts
===================

To list the hosts that would match use the following command::

    pypsh show <hostregex>

Copy file to multiple hosts
===========================

To copy a given file to a group of hosts::

    pypsh copy /tmp/here/myfile.txt "my\.domains\d+\.com" /tmp/remote/file.txt


Installation
============

``Pypsh`` can be installed using ``pip``::

    pip install pypsh

Development
===========

To work on ``pypsh`` checkout the git repository, create a
virtual environment and install the dependencies::

    git clone https://github.com/mfussenegger/pypsh.git
    cd pypsh
    mkvirtualenv pypsh
    pip install -r requirements.txt

Sometimes it is useful to point the ``pypsh`` command to the local development
branch::

    pip install --upgrade --force-reinstall --editable .

But usually it is sufficient to invoke it like this::

    python pypsh/main.py {cmd,copy} ...
