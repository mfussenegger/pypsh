#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import multiprocessing
from time import sleep
from paramiko import (util, SSHConfig, SSHClient, WarningPolicy,
                      BadHostKeyException, SSHException,
                      AuthenticationException as AuthException)
from argh import ArghParser, command
from termcolor import colored


class SSHExecutor(multiprocessing.Process):
    def __init__(self, host, cmd, config):
        super(SSHExecutor, self).__init__()
        self.host = host
        self.cmd = cmd
        self.config = config

    def stop(self):
        self.terminate()

    def run(self):
        sys.exit(self.exec_command())

    def exec_command(self):
        exitcode = 0
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(WarningPolicy)
        try:
            client.connect(self.config.get('hostname'),
                           int(self.config.get('port', 22)),
                           username=self.config.get('user'))
            stdin, stdout, stderr = client.exec_command(self.cmd)
            for i, line in enumerate(stdout):
                line = line.rstrip()
                print("{0}: {1}".format(self.host, line))
            for i, line in enumerate(stderr):
                line = line.rstrip()
                print(colored("{0}: {1}".format(self.host, line), 'red'))
                exitcode = 1
        except IOError as e:
            print(colored('{0}: {1}'.format(self.host, str(e)), 'red'))
            exitcode = 1
        except (BadHostKeyException, AuthException, SSHException) as e:
            print(colored('{0}: {1}'.format(self.host, e.message)), 'red')
            exitcode = 1
        finally:
            client.close()
            return exitcode


@command
def pypsh(hostregex, cmd, serial=False):
    config = SSHConfig()
    config.parse(open(os.path.expanduser('~/.ssh/config')))
    try:
        keys = util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except SSHException as e:
        print(colored('Error in ~/.ssh/known_hosts:', 'red', attrs=['bold']))
        sys.exit(colored(e.message, 'red'))
    hosts = []
    try:
        rex = re.compile(hostregex)
    except:
        sys.exit(colored('Invalid regular expression!', 'red', attrs=['bold']))
    for key in keys:
        if rex.match(key):
            hosts.append(key)

    match_success = 'green' if len(hosts) > 0 else 'red'
    print('>>> {} Hosts matched:'.format(colored(len(hosts), match_success,
                                                 attrs=['bold'])))
    print('')
    print('\n'.join(sorted(hosts)))
    print('')
    print('>>> Starting to execute the command(s):')
    print('')

    processes = []
    for host in hosts:
        p = SSHExecutor(host, cmd, config.lookup(host))
        p.start()
        if serial:
            p.join()
        processes.append(p)

    while multiprocessing.active_children():
        try:
            sleep(0.3)
        except KeyboardInterrupt:
            for p in processes:
                p.stop()
            break

    num_ok = sum([1 for p in processes if p.exitcode == 0])
    failures = sorted([p for p in processes if p.exitcode != 0],
                      key=lambda x: x.host)
    print('>>> {} successful invokations.'.format(colored(num_ok, 'green')))
    print('>>> {} failures:'.format(colored(len(failures), 'red')))
    for p in failures:
        print('\t{}'.format(p.host))


def main():
    p = ArghParser()
    p.set_default_command(pypsh)
    p.dispatch()


if __name__ == '__main__':
    main()
