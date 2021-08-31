#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
Client script
"""

import sys
import paramiko
from db_sync_tool.utility import mode, system, helper, output

ssh_client_origin = None
ssh_client_target = None

default_timeout = 600


def load_ssh_client_origin():
    """
    Loading the origin ssh client
    :return:
    """
    global ssh_client_origin
    ssh_client_origin = load_ssh_client(mode.Client.ORIGIN)
    helper.run_script(mode.Client.ORIGIN, 'before')


def load_ssh_client_target():
    """
    Loading the target ssh client
    :return:
    """
    global ssh_client_target
    ssh_client_target = load_ssh_client(mode.Client.TARGET)
    helper.run_script(mode.Client.TARGET, 'before')


def load_ssh_client(ssh):
    """
    Initializing the given ssh client
    :param ssh: String
    :return:
    """
    _host_name = helper.get_ssh_host_name(ssh, True)
    _ssh_client = paramiko.SSHClient()
    _ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    _ssh_port = _ssh_port = system.config[ssh]['port'] if 'port' in system.config[ssh] else 22
    _ssh_key = None
    _ssh_password = None

    # Check authentication
    if 'ssh_key' in system.config[ssh]:
        _authentication_method = f'{output.CliFormat.BLACK} - ' \
                                 f'(authentication: key){output.CliFormat.ENDC}'
        _ssh_key = system.config[ssh]['ssh_key']
    elif 'password' in system.config[ssh]:
        _authentication_method = f'{output.CliFormat.BLACK} - ' \
                                 f'authentication: password){output.CliFormat.ENDC}'
        _ssh_password = system.config[ssh]['password']
    elif 'ssh_agent' in system.config:
        _authentication_method = f'{output.CliFormat.BLACK} - ' \
                                 f'(authentication: key){output.CliFormat.ENDC}'
    else:
        sys.exit(
            output.message(
                output.Subject.ERROR,
                'Missing SSH authentication. Neither ssh key nor ssh password given.',
                False
            )
        )

    # Try to connect to remote client via paramiko
    try:
        _ssh_client.connect(hostname=system.config[ssh]['host'],
                            username=system.config[ssh]['user'],
                            key_filename=_ssh_key,
                            password=_ssh_password,
                            port=_ssh_port,
                            compress=True,
                            timeout=default_timeout)
        #
        # Workaround for long lasting requests
        # https://stackoverflow.com/questions/50009688/python-paramiko-ssh-session-not-active-after-being-idle-for-many-hours
        #
        _ssh_client.get_transport().set_keepalive(60)

    except paramiko.ssh_exception.AuthenticationException:
        sys.exit(
            output.message(
                output.Subject.ERROR,
                f'SSH authentication for {_host_name} failed',
                False
            )
        )

    output.message(
        output.host_to_subject(ssh),
        f'Initialize remote SSH connection {_host_name}{_authentication_method}',
        True
    )

    return _ssh_client


def close_ssh_clients():
    """
    Closing ssh client sessions
    :return:
    """
    helper.run_script(mode.Client.ORIGIN, 'after')
    if not ssh_client_origin is None:
        ssh_client_origin.close()

    helper.run_script(mode.Client.TARGET, 'after')
    if not ssh_client_target is None:
        ssh_client_target.close()

    helper.run_script(script='after')
