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


def create_local_temporary_data_dir():
    if not os.path.exists(system.default_local_sync_path):
        os.mkdir(system.default_local_sync_path)
