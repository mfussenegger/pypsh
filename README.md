
## Parallel SSH with Regex

Usage:

    ./pypsh.py hostregex cmd

E.g.:

    ./pypsh.py "role\d+\.customer\.your\.domain" "uptime"

This matches every host in the `known_hosts` file against the regex and executes the command.


## Installation & Development:

For now:

    git clone https://github.com/mfussenegger/pypsh.git
    cd pypsh
    mkvirtualenv pypsh
    pip install -r requirements.txt
