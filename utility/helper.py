#!/usr/bin/python

import os, shutil, output, system, database, connect, mode, getpass


#
# CLEAN UP
#
def clean_up():
    connect.remove_origin_database_dump()
    connect.remove_target_database_dump()

# @Deprecated
def remove_temporary_data_dir():
    if os.path.exists(system.default_local_sync_path):
        shutil.rmtree(system.default_local_sync_path)
        output.message(
            output.get_subject().TARGET,
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
