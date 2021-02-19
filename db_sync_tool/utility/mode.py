#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import subprocess
import sys

from db_sync_tool.utility import system, output, helper
from db_sync_tool.remote import system as remote_system


#
# GLOBALS
#

class SyncMode:
    DUMP_LOCAL = 'DUMP_LOCAL'
    DUMP_REMOTE = 'DUMP_REMOTE'
    IMPORT_LOCAL = 'IMPORT_LOCAL'
    IMPORT_REMOTE = 'IMPORT_REMOTE'
    RECEIVER = 'RECEIVER'
    SENDER = 'SENDER'
    PROXY = 'PROXY'


class Client:
    ORIGIN = 'origin'
    TARGET = 'target'
    LOCAL = 'local'


# Default sync mode
sync_mode = SyncMode.RECEIVER


#
# FUNCTIONS
#


def get_sync_mode():
    """
    Returning the sync mode
    :return: String sync_mode
    """
    return sync_mode


def check_sync_mode():
    """
    Checking the sync_mode based on the given configuration
    :return: String subject
    """
    global sync_mode
    _description = ''

    if 'host' in system.config['origin']:
        sync_mode = SyncMode.RECEIVER
        _description = output.CliFormat.BLACK + '(REMOTE ➔ LOCAL)' + output.CliFormat.ENDC
    if 'host' in system.config['target']:
        sync_mode = SyncMode.SENDER
        _description = output.CliFormat.BLACK + '(LOCAL ➔ REMOTE)' + output.CliFormat.ENDC
    if 'host' in system.config['origin'] and 'host' in system.config['target']:
        sync_mode = SyncMode.PROXY
        _description = output.CliFormat.BLACK + '(REMOTE ➔ LOCAL ➔ REMOTE)' + output.CliFormat.ENDC
    if not 'host' in system.config['origin'] and not 'host' in system.config['target']:
        sync_mode = SyncMode.DUMP_LOCAL
        _description = output.CliFormat.BLACK + '(LOCAL, NO TRANSFER/IMPORT)' + output.CliFormat.ENDC
        system.config['is_same_client'] = True
    if 'host' in system.config['origin'] and 'host' in system.config['target'] and \
            system.config['origin']['host'] == system.config['target']['host']:
        if ('port' in system.config['origin'] and 'port' in system.config['target'] and
            system.config['origin']['port'] == system.config['target']['port']) or \
                ('port' not in system.config['origin'] and 'port' not in system.config['target']):
            sync_mode = SyncMode.DUMP_REMOTE
            _description = output.CliFormat.BLACK + '(REMOTE, NO TRANSFER/IMPORT)' + output.CliFormat.ENDC
            system.config['is_same_client'] = True
    if system.config['import'] != '':
        output.message(
            output.Subject.INFO,
            'Import file: ' + system.config['import'],
            True
        )
        if 'host' in system.config['target']:
            sync_mode = SyncMode.IMPORT_REMOTE
            _description = output.CliFormat.BLACK + '(REMOTE, NO TRANSFER)' + output.CliFormat.ENDC
        else:
            sync_mode = SyncMode.IMPORT_LOCAL
            system.config['is_same_client'] = False
            _description = output.CliFormat.BLACK + '(LOCAL, NO TRANSFER)' + output.CliFormat.ENDC

    output.message(
        output.Subject.INFO,
        'Sync mode: ' + sync_mode + ' ' + _description,
        True
    )


def is_remote(client):
    """
    Check if given client is remote client
    :param client: String
    :return: Boolean
    """
    if client == Client.ORIGIN:
        return is_origin_remote()
    elif client == Client.TARGET:
        return is_target_remote()
    elif client == Client.LOCAL:
        return False


def is_target_remote():
    """
    Check if target is remote client
    :return: Boolean
    """
    return sync_mode == SyncMode.SENDER or sync_mode == SyncMode.PROXY or sync_mode == SyncMode.DUMP_REMOTE or \
           sync_mode == SyncMode.IMPORT_REMOTE


def is_origin_remote():
    """
    Check if origin is remote client
    :return: Boolean
    """
    return sync_mode == SyncMode.RECEIVER or sync_mode == SyncMode.PROXY or sync_mode == SyncMode.DUMP_REMOTE or \
           sync_mode == SyncMode.IMPORT_REMOTE


def is_import():
    """
    Check if sync mode is import
    :return: Boolean
    """
    return sync_mode == SyncMode.IMPORT_LOCAL or sync_mode == SyncMode.IMPORT_REMOTE


def run_command(command, client, force_output=False, allow_fail=False):
    """
    Run command depending on the given client
    :param command: String
    :param client: String
    :param force_output: Boolean
    :param allow_fail: Boolean
    :return:
    """
    if system.config['verbose']:
        output.message(
            output.host_to_subject(client),
            output.CliFormat.BLACK + command + output.CliFormat.ENDC,
            True,
            False,
            True
        )

    if is_remote(client):
        if force_output:
            return ''.join(remote_system.run_ssh_command_by_client(client, command).readlines()).strip()
        else:
            return remote_system.run_ssh_command_by_client(client, command)
    else:
        res = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Wait for the process end and print error in case of failure
        out, err = res.communicate()

        if res.wait() != 0 and err.decode() != '' and not allow_fail:
            helper.run_script(script='error')
            sys.exit(output.message(output.Subject.ERROR, err.decode(), False))

        if force_output:
            return out.decode().strip()
