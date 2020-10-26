#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from db_sync_tool.utility import mode, connect, system, output

# Check requirements
try:
    import getpass
    import shutil
    import os
except ImportError:
    sys.exit(
        output.message(
            output.Subject.ERROR,
            'Python requirements missing! Install with: pip3 install -r requirements.txt'
        )
    )


#
# FUNCTIONS
#

def clean_up():
    """
    Clean up
    :return:
    """
    if not mode.is_import():
        connect.remove_target_database_dump()
        if mode.get_sync_mode() == mode.SyncMode.PROXY:
            remove_temporary_data_dir()


def remove_temporary_data_dir():
    """
    Remove temporary data directory for storing database dump files
    :return:
    """
    if os.path.exists(system.default_local_sync_path):
        shutil.rmtree(system.default_local_sync_path)
        output.message(
            output.Subject.LOCAL,
            'Cleaning up',
            True
        )


def clean_up_dump_dir(client, path, num=5):
    """
    Clean up the dump directory from old dump files (only affect .sql and .tar.gz files)
    :param client:
    :param path:
    :param num:
    :return:
    """
    # Distinguish stat command on os system (Darwin|Linux)
    if check_os(client).strip() == 'Darwin':
        _command = get_command(client, 'stat') + ' -f "%Sm %N" ' + path + ' | ' + get_command(client,
                                                                                              'sort') + ' -rn | ' + get_command(
            client, 'grep') + ' -E ".tar.gz|.sql"'
    else:
        _command = get_command(client, 'stat') + ' -c "%y %n" ' + path + ' | ' + get_command(client,
                                                                                             'sort') + ' -rn | ' + get_command(
            client, 'grep') + ' -E ".tar.gz|.sql"'

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
        get_command(client, 'uname') + ' -s',
        client,
        True
    )


def get_command(client, command):
    """
    Get command helper for overriding default commands on the given client
    :param client:
    :param command:
    :return: String command
    """
    if 'console' in system.config['host'][client]:
        if command in system.config['host'][client]['console']:
            return system.config['host'][client]['console'][command]
    return command


def get_dump_dir(client):
    """
    Get database dump directory by client
    :param client:
    :return: String path
    """
    if system.option[f'default_{client}_dump_dir']:
        if not mode.is_remote(client):
            return '/home/' + getpass.getuser() + '/'
        else:
            return '/home/' + system.config['host'][client]['user'] + '/'
    else:
        return system.config['host'][client]['dump_dir']


def check_and_create_dump_dir(client, path):
    """
    Check if a path exists on the client system and creates the given path if necessary
    :param client:
    :param path:
    :return:
    """
    mode.run_command(
        '[ ! -d "' + path + '" ] && mkdir -p "' + path + '"',
        client
    )


def get_ssh_host_name(client, with_user=False):
    """
    Format ssh host name depending on existing client name
    :param client:
    :param with_user:
    :return:
    """
    if with_user:
        _host = system.config['host'][client]['user'] + '@' + system.config['host'][client]['host']
    else:
        _host = system.config['host'][client]['host']

    if 'name' in system.config['host'][client]:
        return output.CliFormat.BOLD + system.config['host'][client][
            'name'] + output.CliFormat.ENDC + output.CliFormat.BLACK + ' (' + _host + ')' + output.CliFormat.ENDC
    else:
        return _host


def create_local_temporary_data_dir():
    """
    Create local temporary data dir
    :return:
    """
    # @ToDo: Combine with check_and_create_dump_dir()
    if not os.path.exists(system.default_local_sync_path):
        os.mkdir(system.default_local_sync_path)
