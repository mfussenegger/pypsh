
=======================
Parallel SSH with Regex
=======================

pypsh is a simple commandline tool to execute a command in parallel on multiple
hosts.

Under the hoods it uses `ssh` via the `paramiko` python library.

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

    pypsh <hostregex> <cmd-to-execute>

E.g.::

    pypsh "role\d+\.customer\.your\.domain" "uptime"

Instead of executing the commands in parallel it is also possible to execute
the commands one after another. To do so use::

    pypsh "role\d+\.customer\.your\.domain" --interval 0.1 cmd "uptime"

Or to wait between the commands (which might be useful when restarting services
like elasticsearch that are part of a cluster)::

    pypsh "role\d+\.customer\.your\.domain" -i 60 cmd "uptime"

`pypsh` can also read from stdin. So it is possible to pipe command into it::

    echo "uptime" | pypsh "myhosts[0-9]"

.. note::

    Piping is only supported if pypsh itself only received one argument.
    Therefore it is not possible to couple it with other parameters like
    `interval`

Copy file to multiple hosts
===========================

To copy a given file to a group of hosts::

    pypsh "my\.domains\d+\.com" copy /tmp/here/myfile.txt /tmp/remote/file.txt

Installation
============

``pypsh`` can be installed using ``pip``::

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

    python pypsh/main.py ...
