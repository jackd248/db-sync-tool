#!/usr/bin/python

import os, shutil, output, system, database, connect

#
# CLEAN UP
#
def clean_up():
    connect.remove_remote_database_dump()
    if not system.option['keep_dump']:
        remove_temporary_data_dir()
    else:
        output.message(
            output.get_subject().INFO,
            'Dump file is saved to: ' + system.default_local_sync_path + database.remote_database_dump_file_name,
            True
        )


def remove_temporary_data_dir():
    if os.path.exists(system.default_local_sync_path):
        shutil.rmtree(system.default_local_sync_path)
        output.message(
            output.get_subject().LOCAL,
            'Cleaning up',
            True
        )