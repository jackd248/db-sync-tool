#!/usr/bin/python

import os, shutil, getpass
from utility import output, system, database, connect, mode


#
# FUNCTIONS
#

def clean_up():
    if not mode.is_import():
        connect.remove_target_database_dump()
        if mode.get_sync_mode() == mode.get_sync_modes().PROXY:
            remove_temporary_data_dir()


def remove_temporary_data_dir():
    if os.path.exists(system.default_local_sync_path):
        shutil.rmtree(system.default_local_sync_path)
        output.message(
            output.get_subject().LOCAL,
            'Cleaning up',
            True
        )


def clean_up_dump_dir(client, path, num=5):
    """
    Clean up the dump directory from old dump files
    :param client:
    :param path:
    :param num:
    :return:
    """
    # Distinguish stat command on os system (Darwin|Linux)
    if check_os(client).strip() == 'Darwin':
        _command = 'stat -f "%Sm %N" ' + path + ' | sort -rn'
    else:
        _command = 'stat -c "%y %n" ' + path + ' | sort -rn'

    # List files in directory sorted by change date
    _files = mode.run_command(
        _command,
        client,
        True
    ).splitlines()

    for i in range(len(_files)):
        _filename = _files[i].rsplit(' ', 1)[-1]

        # Remove oldest files chosen by keep_dumps count
        if not i < num:
            mode.run_command(
                'rm ' + _filename,
                client
            )


def check_os(client):
    """
    Check which system is running (Linux|Darwin)
    :param client:
    :return:
    """
    return mode.run_command(
        'uname -s',
        client,
        True
    )

def get_command(target, command):
    if 'console' in system.config['host'][target]:
        if command in system.config['host'][target]['console']:
            return system.config['host'][target]['console'][command]
    return command


def get_origin_dump_dir():
    if system.option['default_origin_dump_dir']:
        if not mode.is_origin_remote():
            return '/home/' + getpass.getuser() + '/'
        else:
            return '/home/' + system.config['host']['origin']['user'] + '/'
    else:
        return system.config['host']['origin']['dump_dir']


def get_target_dump_dir():
    if system.option['default_target_dump_dir']:
        if not mode.is_target_remote():
            return '/home/' + getpass.getuser() + '/'
        else:
            return '/home/' + system.config['host']['target']['user'] + '/'
    else:
        return system.config['host']['target']['dump_dir']


def check_and_create_dump_dir(client, path):
    """
    Check if a path exists on the client system and creates the given path if necessary
    :param client:
    :param path:
    :return:
    """
    mode.run_command(
        '[ ! -d "' + path + '" ] && mkdir - p "' + path + '"',
        client
    )


def create_local_temporary_data_dir():
    if not os.path.exists(system.default_local_sync_path):
        os.mkdir(system.default_local_sync_path)
