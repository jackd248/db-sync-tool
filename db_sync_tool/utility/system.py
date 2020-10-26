#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from db_sync_tool.utility import log, parser, mode, helper, output

# Check requirements
try:
    import json
    import os
    import getpass
except ImportError:
     sys.exit(
         output.message(
             output.Subject.ERROR,
             'Python requirements missing! Install with: pip3 install -r requirements.txt'
         )
     )

#
# GLOBALS
#

config = {}
option = {
    'verbose': False,
    'mute': False,
    'use_origin_ssh_key': False,
    'use_target_ssh_key': False,
    'keep_dump': False,
    'dump_name': '',
    'import': '',
    'link_hosts': '',
    'default_origin_dump_dir': True,
    'default_target_dump_dir': True,
    'check_dump': True,
    'is_same_client': False,
    'config_file_path': None,
    'ssh_password': {
        'origin': None,
        'target': None
    }
}

#
# DEFAULTS
#

default_local_sync_path = os.path.abspath(os.getcwd()) + '/.sync/'


#
# FUNCTIONS
#

def check_target_configuration():
    """
    Checking target database configuration
    :return:
    """
    parser.get_database_configuration(mode.Client.TARGET)


def get_configuration(host_config):
    """
    Checking configuration information by file or dictionary
    :param host_config: Dictionary
    :return:
    """
    if not option['config_file_path'] is None:
        if os.path.isfile(option['config_file_path']):
            with open(option['config_file_path'], 'r') as read_file:
                config['host'] = json.load(read_file)
                output.message(
                    output.Subject.LOCAL,
                    'Loading host configuration',
                    True
                )

                check_options()
        else:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Local host configuration not found: {option["config_file_path"]}',
                    False
                )
        )

    if host_config:
        config['host'] = host_config

    log.get_logger().info('Starting db_sync_tool')
    output.message(
        output.Subject.INFO,
        'Configuration: ' + option['config_file_path'],
        True,
        True
    )


def check_options():
    """
    Checking configuration provided file
    :return:
    """
    if 'dump_dir' in config['host']['origin']:
        option['default_origin_dump_dir'] = False

    if 'dump_dir' in config['host']['target']:
        option['default_target_dump_dir'] = False

    if 'check_dump' in config['host']:
        option['check_dump'] = config['host']['check_dump']

    if option['link_hosts'] != '':
        link_configuration_with_hosts()

    mode.check_sync_mode()
    check_authorization(mode.Client.ORIGIN)
    check_authorization(mode.Client.TARGET)


def check_authorization(client):
    """
    Checking arguments and fill options array
    :param client: String
    :return:
    """
    # only need authorization if client is remote
    if mode.is_remote(client):
        # Workaround
        if (mode.get_sync_mode() == mode.SyncMode.DUMP_REMOTE and client == mode.Client.TARGET) or (
                mode.get_sync_mode() == mode.SyncMode.DUMP_LOCAL and client == mode.Client.ORIGIN) or (
                mode.get_sync_mode() == mode.SyncMode.IMPORT_REMOTE and client == mode.Client.ORIGIN):
            return

        # ssh key authorization
        if 'ssh_key' in config['host'][client]:
            _ssh_key = config['host'][client]['ssh_key']
            if os.path.isfile(_ssh_key):
                option[f'use_{client}_ssh_key'] = True
            else:
                sys.exit(
                    output.message(
                        output.Subject.ERROR,
                        f'SSH {client} private key not found: {_ssh_key}',
                        False
                    )
                )
        # plain password authorization
        elif 'password' in config['host'][client]:
            option['ssh_password'][client] = config['host'][client]['password']
        # user input authorization
        else:
            option['ssh_password'][client] = get_password_by_user(client)

        if mode.get_sync_mode() == mode.SyncMode.DUMP_REMOTE and client == mode.Client.ORIGIN:
            option['ssh_password'][mode.Client.TARGET] = option['ssh_password'][mode.Client.ORIGIN]


def get_password_by_user(client):
    """
    Getting password by user input
    :param client: String
    :return: String password
    """
    _password = getpass.getpass(
        output.message(
            output.Subject.INFO,
            'SSH password ' + helper.get_ssh_host_name(client, True) + ': ',
            False
        )
    )

    while _password.strip() == '':
        output.message(
            output.Subject.WARNING,
            'Password seems to be empty. Please enter a valid password.',
            True
        )

        _password = getpass.getpass(
            output.message(
                output.Subject.INFO,
                'SSH password ' + helper.get_ssh_host_name(client, True) + ': ',
                False
            )
        )

    return _password


def check_args_options(args):
    """
    Checking arguments and fill options array
    :param args:
    :return:
    """
    global option
    global default_local_sync_path

    if not args.file is None:
        option['config_file_path'] = args.file

    option['verbose'] = args.verbose

    option['mute'] = args.mute

    if not args.importfile is None:
        option['import'] = args.importfile

    if not args.dumpname is None:
        option['dump_name'] = args.dumpname

    if not args.hosts is None:
        option['link_hosts'] = args.hosts

    if not args.keepdump is None:
        default_local_sync_path = args.keepdump

        # Adding trailing slash if necessary
        if default_local_sync_path[-1] != '/':
            default_local_sync_path += '/'

        option['keep_dump'] = True
        output.message(
            output.Subject.INFO,
            '"Keep dump" option chosen',
            True
        )


def link_configuration_with_hosts():
    """
    Merging the hosts definition with the given configuration file
    :return:
    """
    if os.path.isfile(option['link_hosts']):
        with open(option['link_hosts'], 'r') as read_file:
            _hosts = json.load(read_file)
            if 'link' in config['host']['origin']:
                _host_name = str(config['host']['origin']['link']).replace('@','')
                if _host_name in _hosts:
                    config['host']['origin'] = {**config['host']['origin'], **_hosts[_host_name]}

            if 'link' in config['host']['target']:
                _host_name = str(config['host']['target']['link']).replace('@','')
                if _host_name in _hosts:
                    config['host']['target'] = {**config['host']['target'], **_hosts[_host_name]}


