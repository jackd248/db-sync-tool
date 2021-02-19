#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import sys
import json
import os
import getpass
from db_sync_tool.utility import log, parser, mode, helper, output

#
# GLOBALS
#

config = {
    'verbose': False,
    'mute': False,
    'keep_dump': False,
    'dump_name': '',
    'import': '',
    'link_hosts': '',
    'default_origin_dump_dir': True,
    'default_target_dump_dir': True,
    'check_dump': True,
    'is_same_client': False,
    'config_file_path': None,
    'clear_database': False,
    'ssh_password': {
        'origin': None,
        'target': None
    }
}

#
# DEFAULTS
#

default_local_sync_path = '/tmp/'


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
    global config

    if config['config_file_path'] is None and host_config == {}:
        sys.exit(
            output.message(
                output.Subject.ERROR,
                f'Configuration is missing, use a separate file or provide host parameter',
                False
            )
        )

    if host_config:
        config.update(host_config)

    _config_file_path = config['config_file_path']
    if not _config_file_path is None:
        if os.path.isfile(_config_file_path):
            with open(_config_file_path, 'r') as read_file:
                config.update(json.load(read_file))
                output.message(
                    output.Subject.LOCAL,
                    f'Loading host configuration {output.CliFormat.BLACK}{_config_file_path}{output.CliFormat.ENDC}',
                    True
                )
        else:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Local configuration not found: {config["config_file_path"]}',
                    False
                )
            )

    check_options()
    helper.run_script(script='before')
    log.get_logger().info('Starting db_sync_tool')


def check_options():
    """
    Checking configuration provided file
    :return:
    """
    global config
    if 'dump_dir' in config['origin']:
        config['default_origin_dump_dir'] = False

    if 'dump_dir' in config['target']:
        config['default_target_dump_dir'] = False

    if 'check_dump' in config:
        config['check_dump'] = config['check_dump']

    link_configuration_with_hosts()
    mode.check_sync_mode()


def check_authorizations():
    """
    Checking authorization for clients
    :return:
    """
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
        # Workaround if no authorization is needed
        if (mode.get_sync_mode() == mode.SyncMode.DUMP_REMOTE and client == mode.Client.TARGET) or (
                mode.get_sync_mode() == mode.SyncMode.DUMP_LOCAL and client == mode.Client.ORIGIN) or (
                mode.get_sync_mode() == mode.SyncMode.IMPORT_REMOTE and client == mode.Client.ORIGIN):
            return

        # ssh key authorization
        if 'ssh_key' in config[client]:
            _ssh_key = config[client]['ssh_key']
            if not os.path.isfile(_ssh_key):
                sys.exit(
                    output.message(
                        output.Subject.ERROR,
                        f'SSH {client} private key not found: {_ssh_key}',
                        False
                    )
                )
        elif 'password' in config[client]:
            config[client]['password'] = config[client]['password']
        else:
            # user input authorization
            config[client]['password'] = get_password_by_user(client)

        if mode.get_sync_mode() == mode.SyncMode.DUMP_REMOTE and client == mode.Client.ORIGIN and 'password' in config[mode.Client.ORIGIN]:
            config[mode.Client.TARGET]['password'] = config[mode.Client.ORIGIN]['password']


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


def check_args_options(config_file=None,
                       verbose=False,
                       yes=False,
                       mute=False,
                       import_file=None,
                       dump_name=None,
                       keep_dump=None,
                       host_file=None,
                       clear=False):
    """
    Checking arguments and fill options array
    :param config_file:
    :param verbose:
    :param yes:
    :param mute:
    :param import_file:
    :param dump_name:
    :param keep_dump:
    :param host_file:
    :param clear:
    :return:
    """
    global config
    global default_local_sync_path

    if not config_file is None:
        config['config_file_path'] = config_file

    if not verbose is None:
        config['verbose'] = verbose

    if not yes is None:
        config['yes'] = yes

    if not mute is None:
        config['mute'] = mute

    if not import_file is None:
        config['import'] = import_file

    if not dump_name is None:
        config['dump_name'] = dump_name

    if not host_file is None:
        config['link_hosts'] = host_file

    if not clear is None:
        config['clear_database'] = clear

    if not keep_dump is None:
        default_local_sync_path = keep_dump

        # Adding trailing slash if necessary
        if default_local_sync_path[-1] != '/':
            default_local_sync_path += '/'

        config['keep_dump'] = True
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
    if ('link' in config['origin'] or 'link' in config['target']) and config['link_hosts'] == '':
        # Try to find default hosts.json file in same directory
        sys.exit(
            output.message(
                output.Subject.ERROR,
                f'Missing hosts file for linking hosts with configuration. '
                f'Use the "-o" / "--hosts" argument to define the filepath for the hosts file, when using a link parameter within the configuration.',
                False
            )
        )

    if config['link_hosts'] != '':
        if os.path.isfile(config['link_hosts']):
            with open(config['link_hosts'], 'r') as read_file:
                _hosts = json.load(read_file)
                output.message(
                    output.Subject.INFO,
                    f'Linking configuration with hosts {output.CliFormat.BLACK}{config["link_hosts"]}{output.CliFormat.ENDC}',
                    True
                )
                if 'link' in config['origin']:
                    _host_name = str(config['origin']['link']).replace('@','')
                    if _host_name in _hosts:
                        config['origin'] = {**config['origin'], **_hosts[_host_name]}

                if 'link' in config['target']:
                    _host_name = str(config['target']['link']).replace('@','')
                    if _host_name in _hosts:
                        config['target'] = {**config['target'], **_hosts[_host_name]}
        else:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Local host file not found: {config["link_hosts"]}',
                    False
                )
            )



