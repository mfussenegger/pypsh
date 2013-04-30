
=======================
Parallel SSH with Regex
=======================

To execute a command on a group of hosts matching a given regular expression::

    pypsh cmd <hostregex> <cmd-to-execute>

E.g.::

    pypsh cmd "role\d+\.customer\.your\.domain" "uptime"

Or to copy a given file to a group of hosts::

    pypsh copy /tmp/here/myfile.txt "my\.domains\d+\.com" /tmp/remote/file.txt



The command or file copy operation will be executed on any host that is in the
`known_hosts` file and matches the given regular expression.

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
