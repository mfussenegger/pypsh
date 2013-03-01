
=======================
Parallel SSH with Regex
=======================

Usage::

    pypsh hostregex cmd

E.g.::

    pypsh "role\d+\.customer\.your\.domain" "uptime"

This matches every host in the `known_hosts` file against the regex and
executes the command.

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

    python pypsh/main.py
