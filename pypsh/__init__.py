#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1.0'

import os
import sys
import re
import multiprocessing
from time import sleep
from paramiko import util, SSHConfig, SSHClient, WarningPolicy
from argh import ArghParser, command


class SSHExecutor(multiprocessing.Process):
    def __init__(self, host, cmd, config):
        super(SSHExecutor, self).__init__()
        self.host = host
        self.cmd = cmd
        self.config = config

    def stop(self):
        self.terminate()

    def run(self):
        exec_command(self.cmd, self.config, self.host)


@command
def pypsh(hostregex, cmd):
    config = SSHConfig()
    config.parse(open(os.path.expanduser('~/.ssh/config')))
    keys = util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    hosts = []
    for key in keys:
        if re.match(hostregex, key):
            hosts.append(key)

    processes = []
    for host in hosts:
        p = SSHExecutor(host, cmd, config.lookup(host))
        p.start()
        processes.append(p)

    while multiprocessing.active_children():
        try:
            sleep(0.3)
        except KeyboardInterrupt:
            for p in processes:
                p.stop()
            sys.exit()


def exec_command(cmd, hostconfig, host):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(WarningPolicy)
    client.connect(hostconfig.get('hostname'),
                   int(hostconfig.get('port', 22)),
                   username=hostconfig.get('user'))
    stdin, stdout, stderr = client.exec_command(cmd)
    for i, line in enumerate(stdout):
        line = line.rstrip()
        print("{0}: {1}".format(host, line))
    for i, line in enumerate(stderr):
        line = line.rstrip()
        print("{0}: {1}".format(host, line))
    client.close()


def main():
    p = ArghParser()
    p.set_default_command(pypsh)
    p.dispatch()


if __name__ == '__main__':
    main()
