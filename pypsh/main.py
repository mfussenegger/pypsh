#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import multiprocessing
from numbers import Number
from time import sleep
from functools import partial
from paramiko import (util, SSHConfig, SSHClient, WarningPolicy,
                      BadHostKeyException, SSHException,
                      AuthenticationException as AuthException)
from argh import ArghParser, command
from termcolor import colored


class Executor(multiprocessing.Process):
    """ abstract class that connects via ssh to a given host and executes
    `exec_command()`

    exec_command has to be overwritten in a subclass to do something useful.
    """

    def __init__(self, host, config):
        super(Executor, self).__init__()
        self.host = host
        self.config = config

    def stop(self):
        self.terminate()

    def run(self):
        sys.exit(self._exec())

    def exec_command(self):
        """overwrite this method to implement specific functionality

        this method has to return a tuple with 3 iterables.
        (stdin, stdout, stderr)
        """

    def _exec(self):
        exitcode = 0
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(WarningPolicy)
        try:
            client.connect(self.config.get('hostname'),
                           int(self.config.get('port', 22)),
                           username=self.config.get('user'))
            stdin, stdout, stderr = self.exec_command(client)
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


class SSHExecutor(Executor):
    """ execute a simple command via ssh """

    def __init__(self, host, config, cmd):
        super(SSHExecutor, self).__init__(host, config)
        self.cmd = cmd

    def exec_command(self, client):
        return client.exec_command(self.cmd)


class CopyExecutor(Executor):
    """ copy a file from source to destination via ssh/sftp """

    def __init__(self, host, config, source, destination):
        super(CopyExecutor, self).__init__(host, config)
        self.source = source
        self.destination = destination

    def exec_command(self, client):
        sftp = client.open_sftp()
        sftp.put(self.source, self.destination)
        sftp.close()
        return ([], ['Copied to {}'.format(self.host)], [])


def get_hosts(hostregex):
    """return all hosts that are in the known_hosts file and match the given
    regex

    """
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
    return hosts


def print_result(processes):
    num_ok = sum([1 for p in processes if p.exitcode == 0])
    failures = sorted([p for p in processes if p.exitcode != 0],
                      key=lambda x: x.host)
    print('>>> {} successful invocations.'.format(colored(num_ok, 'green')))
    print('>>> {} failures:'.format(colored(len(failures), 'red')))
    for p in failures:
        print('\t{}'.format(p.host))


def start_procs(serial, hosts, starter_func, wait=0.0):
    config = SSHConfig()
    config.parse(open(os.path.expanduser('~/.ssh/config')))

    try:
        wait = float(wait)
    except ValueError:
        pass

    processes = []
    for host in hosts:
        process = starter_func(host, config.lookup(host))
        process.start()
        if serial or wait > 0.0:
            process.join()
            if isinstance(wait, Number):
                sleep(wait)
        processes.append(process)

    while multiprocessing.active_children():
        try:
            sleep(0.3)
        except KeyboardInterrupt:
            for p in processes:
                p.stop()
            break
    return processes


@command
def cmd(hostregex, cmd, serial=False, wait=0.0):
    hosts = get_hosts(hostregex)
    print('>>> Starting to execute the command(s):')
    print('')

    cmd_executer = partial(SSHExecutor, cmd=cmd)
    processes = start_procs(serial, hosts, cmd_executer, wait=wait)
    print_result(processes)


@command
def copy(source, hostregex, destination, serial=False):
    hosts = get_hosts(hostregex)
    if not os.path.isfile(source):
        print(colored('>>> Source {} does not exist'.format(source), 'red'))
        sys.exit(1)
    print('>>> Starting to copy the file:')
    print('')

    cmd_executer = partial(CopyExecutor,
                           source=source,
                           destination=destination)
    processes = start_procs(serial, hosts, cmd_executer)
    print_result(processes)


@command
def show(hostregex):
    get_hosts(hostregex)


def main():
    p = ArghParser()
    p.add_commands([cmd, copy, show])
    p.dispatch()


if __name__ == '__main__':
    main()
