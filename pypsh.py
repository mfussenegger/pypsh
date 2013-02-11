#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from multiprocessing import Pool
from functools import partial
from paramiko import util, SSHConfig, SSHClient, WarningPolicy
from argh import ArghParser, command


@command
def pypsh(hostregex, cmd):
    config = SSHConfig()
    config.parse(open(os.path.expanduser('~/.ssh/config')))
    keys = util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    hosts = []
    for key in keys:
        if re.match(hostregex, key):
            hosts.append(key)

    pool = Pool(len(hosts))
    func = partial(exec_command, cmd, config)
    pool.map(func, hosts, 1)
    pool.close()
    pool.join()


def exec_command(cmd, config, host):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(WarningPolicy)
    hostconfig = config.lookup(host)
    client.connect(hostconfig.get('hostname'),
                    int(hostconfig.get('port', 22)),
                    username=hostconfig.get('user'))
    stdin, stdout, stderr = client.exec_command(cmd)
    for i, line in enumerate(stdout):
        line = line.rstrip()
        print("{0}: {1}".format(i, line))
    client.close()


def main():
    p = ArghParser()
    p.set_default_command(pypsh)
    p.dispatch()


if __name__ == '__main__':
    main()
