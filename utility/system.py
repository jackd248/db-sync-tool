#!/usr/bin/python

import sys, json, os, getpass, output, connect

#
# GLOBALS
#
class framework:
    TYPO3 = 1
    SYMFONY = 2

config = {}
option = {
    'verbose': False,
    'use_ssh_key': False,
    'keep_dump': False,
    'framework': framework.TYPO3
}
remote_ssh_password = None

#
# DEFAULTS
#
default_local_host_file_path = 'host.json'
default_local_sync_path = os.path.abspath(os.getcwd()) + '/.sync/'
default_ignore_database_tables = [
    'sys_domain',
    'cf_cache_hash',
    'cf_cache_hash_tags',
    'cf_cache_news_category',
    'cf_cache_news_category_tags',
    'cf_cache_pages',
    'cf_cache_pagesection',
    'cf_cache_pagesection_tags',
    'cf_cache_pages_tags',
    'cf_cache_rootline',
    'cf_cache_rootline_tags',
    'cf_extbase_datamapfactory_datamap',
    'cf_extbase_datamapfactory_datamap_tags',
    'cf_extbase_object',
    'cf_extbase_object_tags',
    'cf_extbase_reflection',
    'cf_extbase_reflection_tags',
]


#
# CHECK CONFIGURATION
#
def check_configuration():
    get_host_configuration()
    load_pip_modules()
    if not option['use_ssh_key']:
        get_remote_password()


    if option['framework'] == framework.TYPO3:
        sys.path.append('./parser')
        from parser import typo3

        typo3.check_local_configuration()
        connect.get_ssh_client()
        typo3.check_remote_configuration()

    elif option['framework'] == framework.SYMFONY:
        sys.path.append('./parser')
        from parser import symfony

        symfony.check_local_configuration()
        connect.get_ssh_client()
        symfony.check_remote_configuration()

def get_host_configuration():
    print(default_local_host_file_path)
    if os.path.isfile(default_local_host_file_path):
        with open(default_local_host_file_path, 'r') as read_file:
            config['host'] = json.load(read_file)
            output.message(
                output.get_subject().LOCAL,
                'Loading host configuration',
                True
            )

            # check if custom ignore_table configuration is provided
            if 'ignore_table' in config['host']:
                config['ignore_table'] = config['host']['ignore_table']
            else:
                config['ignore_table'] = default_ignore_database_tables

            # check if ssh key authorization should be used
            if 'ssh_key' in config['host']:
                if os.path.isfile(config['host']['ssh_key']):
                    option['use_ssh_key'] = True
                else:
                    sys.exit(
                        output.message(
                            output.get_subject().ERROR,
                            'SSH private key not found',
                            False
                        )
                    )

            # check framework type
            if 'type' in config['host']:
                if config['host']['type'] == 'TYPO3':
                    option['framework'] = framework.TYPO3
                elif config['host']['type'] == 'Symfony':
                    option['framework'] = framework.SYMFONY
                else:
                    sys.exit(
                        output.message(
                            output.get_subject().ERROR,
                            'Framework type not supported',
                            False
                        )
                    )
            else:
                option['framework'] = framework.TYPO3

    else:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Local host configuration not found',
                False
            )
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


def get_remote_password():
    global remote_ssh_password

    _password = getpass.getpass(
        output.message(
            output.get_subject().INFO,
            'SSH password ' + config['host']['remote']['user'] + '@' + config['host']['remote']['host'] + ': ',
            False
        )
    )

    while _password.strip() is '':
        output.message(
            output.get_subject().WARNING,
            'Password is empty. Please enter a valid password.',
            True
        )

        _password = getpass.getpass(
            output.message(
                output.get_subject().INFO,
                'SSH password ' + config['host']['remote']['user'] + '@' + config['host']['remote']['host'] + ': ',
                False
            )
        )

    remote_ssh_password = _password


def check_options(args):
    global option
    global default_local_host_file_path
    global default_local_sync_path

    if not args.file is None:
        default_local_host_file_path = args.file

    if not args.verbose is None:
        option['verbose'] = True

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


def create_temporary_data_dir():
    if not os.path.exists(default_local_sync_path):
        os.mkdir(default_local_sync_path)

def get_framework():
    return framework