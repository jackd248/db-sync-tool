#!/usr/bin/python

import os, shutil, output, system, database, connect

#
# CLEAN UP
#
def clean_up():
    connect.remove_origin_database_dump()
    if not system.option['keep_dump']:
        remove_temporary_data_dir()
    else:
        output.message(
            output.get_subject().INFO,
            'Dump file is saved to: ' + system.default_local_sync_path + database.origin_database_dump_file_name,
            True
        )


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
        return '/home/' + system.config['host']['origin']['user'] + '/'
    else:
        return system.config['host']['origin']['dump_dir']