#!/usr/bin/python

import sys, json, os, getpass
from utility import output, log, mode, parser, helper

#
# GLOBALS
#

config = {}
option = {
    'verbose': False,
    'use_origin_ssh_key': False,
    'use_target_ssh_key': False,
    'keep_dump': False,
    'dump_name': '',
    'import': '',
    'default_origin_dump_dir': True,
    'default_target_dump_dir': True,
    'check_dump': True,
    'is_same_client': False,
    'ssh_password': {
        'origin': None,
        'target': None
    }
}

#
# DEFAULTS
#

default_local_host_file_path = 'host.json'
default_local_sync_path = os.path.abspath(os.getcwd()) + '/.sync/'


#
# FUNCTIONS
#

def check_configuration():
    load_pip_modules()
    get_host_configuration()
    if not option['use_origin_ssh_key'] and mode.is_origin_remote() and option['import'] == '':
        option['ssh_password']['origin'] = get_password(mode.get_clients().ORIGIN)

        if mode.get_sync_mode() == mode.get_sync_modes().DUMP_REMOTE:
            option['ssh_password']['target'] = option['ssh_password']['origin']


    if not option['use_target_ssh_key'] and mode.is_target_remote() and mode.get_sync_mode() != mode.get_sync_modes().DUMP_REMOTE:
        option['ssh_password']['target'] = get_password(mode.get_clients().TARGET)

    if not mode.is_import():
        # first get data configuration for origin client
        parser.get_database_configuration(mode.get_clients().ORIGIN)


def check_target_configuration():
    parser.get_database_configuration(mode.get_clients().TARGET)


def get_host_configuration():
    if os.path.isfile(default_local_host_file_path):
        with open(default_local_host_file_path, 'r') as read_file:
            config['host'] = json.load(read_file)
            output.message(
                output.get_subject().LOCAL,
                'Loading host configuration',
                True
            )

            check_options()
    else:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Local host configuration not found',
                False
            )
        )

    log.get_logger().info('Starting db_sync_tool')
    output.message(
        output.get_subject().INFO,
        'Configuration: ' + default_local_host_file_path,
        True,
        True
    )

def load_pip_modules():
    import importlib
    import subprocess

    try:
        import pip
    except ImportError:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Pip is not installed',
                False
            )
        )

    output.message(
        output.get_subject().LOCAL,
        'Checking pip modules',
        True
    )

    package = 'paramiko'

    try:
        globals()[package] = importlib.import_module(package)

    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        sys.exit(
            output.message(
                output.get_subject().INFO,
                'First install of additional pip modules completed. Please re-run the script.',
                False
            )
        )


def get_password(client):
    _password = getpass.getpass(
        output.message(
            output.get_subject().INFO,
            'SSH password ' + helper.get_ssh_host_name(client, True) + ': ',
            False
        )
    )

    while _password.strip() == '':
        output.message(
            output.get_subject().WARNING,
            'Password is empty. Please enter a valid password.',
            True
        )

        _password = getpass.getpass(
            output.message(
                output.get_subject().INFO,
                'SSH password ' + helper.get_ssh_host_name(client, True) + ': ',
                False
            )
        )

    return _password


def check_options():
    # check if ssh key authorization should be used
    if 'ssh_key' in config['host']['origin']:
        if os.path.isfile(config['host']['origin']['ssh_key']):
            option['use_origin_ssh_key'] = True
        else:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH origin private key not found',
                    False
                )
            )

    if 'ssh_key' in config['host']['target']:
        if os.path.isfile(config['host']['origin']['ssh_key']):
            option['use_target_ssh_key'] = True
        else:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH target private key not found',
                    False
                )
            )

    if 'dump_dir' in config['host']['origin']:
        option['default_origin_dump_dir'] = False

    if 'dump_dir' in config['host']['target']:
        option['default_target_dump_dir'] = False

    if 'check_dump' in config['host']:
        option['check_dump'] = config['host']['check_dump']

    mode.check_sync_mode()


def check_args_options(args):
    """
    Checking arguments and fill options array
    :param args:
    :return:
    """
    global option
    global default_local_host_file_path
    global default_local_sync_path

    if not args.file is None:
        default_local_host_file_path = args.file

    if not args.verbose is None:
        option['verbose'] = True

    if not args.importfile is None:
            option['import'] = args.importfile

    if not args.dumpname is None:
        option['dump_name'] = args.dumpname

    if not args.keepdump is None:
        default_local_sync_path = args.keepdump

        if default_local_sync_path[-1] != '/':
            default_local_sync_path += '/'

        option['keep_dump'] = True
        output.message(
            output.get_subject().INFO,
            '"Keep dump" option chosen',
            True
        )
