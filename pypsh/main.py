#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import multiprocessing
import select
from threading import Thread
from argparse import ArgumentParser
from time import sleep
from functools import partial
from paramiko import (util, SSHConfig, SSHClient, WarningPolicy,
                      BadHostKeyException, SSHException,
                      AuthenticationException as AuthException)
from termcolor import colored


class Printer(object):

    def __init__(self, host, stdout, stderr):
        def printer(stream, color):
            hostpart = colored("[{0}]".format(host), color) + ": "
            for line in stream:
                line = line.rstrip()
                print(hostpart + line)
        self.printers = [
            Thread(target=printer, args=(stdout, 'green')),
            Thread(target=printer, args=(stderr, 'red'))
        ]
        self.stdout = stdout
        self.stderr = stderr

    def loop(self):
        for p in self.printers:
            p.daemon = True
            p.start()
        for p in self.printers:
            p.join()
        if hasattr(self.stdout, 'close'):
            self.stdout.close()
        if hasattr(self.stderr, 'close'):
            self.stderr.close()


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
        (stdout, stderr, channel)
        """

    def _exec(self):
        exitcode = 0
        client = SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(WarningPolicy())
        try:
            client.connect(self.config.get('hostname'),
                           int(self.config.get('port', 22)),
                           username=self.config.get('user'))
            stdout, stderr, channel = self.exec_command(client)
            Printer(self.host, stdout, stderr).loop()
            if channel:
                exitcode = channel.recv_exit_status()
        except IOError as e:
            print(colored('{0}: {1}'.format(self.host, str(e)), 'red'))
            exitcode = 1
        except (BadHostKeyException, AuthException, SSHException) as e:
            print(colored('{0}: {1}'.format(self.host, e.message)), 'red')
            exitcode = 1
        except Exception as e:
            print(colored('{0}: {1}'.format(self.host, e.message)), 'red')
            exitcode = 1
        finally:
            client.close()
            return exitcode


class SSHExecutor(Executor):
    """ execute a simple command via ssh """

    def __init__(self, host, config, cmd, pty):
        super(SSHExecutor, self).__init__(host, config)
        self.cmd = cmd
        self.get_pty = pty
        self.timeout = None

    def exec_command(self, client):
        chan = client.get_transport().open_session()
        if self.get_pty:
            chan.get_pty()
        chan.settimeout(self.timeout)
        chan.exec_command(self.cmd)
        stdin = chan.makefile('wb', -1)
        stdout = chan.makefile('r', -1)
        stderr = chan.makefile_stderr('r', -1)
        stdin.close()
        return stdout, stderr, chan


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
        return (['Copied to {}'.format(self.host)], [], None)


RE_HOST_PORT = re.compile('\[(.*)\]:\d+.*')


def get_hosts(hostregex):
    """return all hosts that are in the known_hosts file and match the given
    regex.

    Will return an empty list if no hosts matched.
    """
    try:
        keys = util.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
    except SSHException as e:
        print(colored('Error in ~/.ssh/known_hosts:', 'red', attrs=['bold']))
        sys.exit(colored(e.message, 'red'))
    hosts = []
    try:
        rex = re.compile(hostregex)
    except re.error:
        sys.exit(colored('Invalid regular expression!', 'red', attrs=['bold']))
    for key in keys:
        custom_port_match = RE_HOST_PORT.match(key)
        if custom_port_match:
            key = custom_port_match.group(1)
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


def start_procs(interval, hosts, starter_func):
    config = SSHConfig()
    config.parse(open(os.path.expanduser('~/.ssh/config')))

    processes = []
    for host in hosts:
        process = starter_func(host, config.lookup(host))
        process.start()
        if interval > 0.0:
            process.join()
            sleep(interval)
        processes.append(process)

    while multiprocessing.active_children():
        try:
            sleep(0.3)
        except KeyboardInterrupt:
            for p in processes:
                p.stop()
            break
    return processes


def cmd(hosts, cmd, interval=0.0, pty=False):
    print('>>> Starting to execute the command(s):')
    print('')
    cmd_executer = partial(SSHExecutor, cmd=cmd, pty=pty)
    processes = start_procs(interval, hosts, cmd_executer)
    print_result(processes)


def copy(source, hosts, destination, interval=0.0):
    if not os.path.isfile(source):
        print(colored('>>> Source {} does not exist'.format(source), 'red'))
        sys.exit(1)
    print('>>> Starting to copy the file:')
    print('')

    cmd_executer = partial(CopyExecutor,
                           source=source,
                           destination=destination)
    processes = start_procs(interval, hosts, cmd_executer)
    print_result(processes)


def dispatch(args):
    hosts = get_hosts(args.hostregex)
    if 'command' in args:
        cmd(hosts, args.command, args.interval)
    else:
        copy(args.source, hosts, args.destination, args.interval)


def create_parser():
    parser = ArgumentParser(description='parallel ssh command execution')
    parser.add_argument('hostregex', type=str,
                        help='regular expression to match the hostnames')
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=0.0,
        help=('time to wait between command execution on the different hosts.'
              '0 means no wait time and everything is executed in parallel'))
    subparsers = parser.add_subparsers(help='sub-command help')

    cmd_subcommand = subparsers.add_parser(
        'cmd', help='execute a command on multiple hosts'
    )
    cmd_subcommand.set_defaults(func=dispatch)
    cmd_subcommand.add_argument('command', type=str, help='command to execute')
    cmd_subcommand.add_argument('--pty', action='count',
                                help='attach pty', default=False)

    copy_subcommand = subparsers.add_parser(
        'copy', help='copy a file from the local machine to multiple hosts'
    )
    copy_subcommand.set_defaults(func=dispatch)
    copy_subcommand.add_argument('source', type=str,
                                 help='path to the file on the local machine')
    copy_subcommand.add_argument('destination', type=str,
                                 help='path to the file on the remote hosts')
    return parser


def main():
    if len(sys.argv) == 2:
        hosts = get_hosts(sys.argv[1])
        if hosts:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                if line:
                    cmd(hosts, line, False)
                else:
                    sys.exit(0)
    elif len(sys.argv) == 3:
        # "pypsh <hostregex> <command>" should work too
        hosts = get_hosts(sys.argv[1])
        if hosts and sys.argv[2] != 'help':
            cmd(hosts, sys.argv[2], False)
            sys.exit(0)
    parser = create_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
