#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
Mode script
"""

import subprocess
import sys

from db_sync_tool.utility import system, output, helper
from db_sync_tool.remote import system as remote_system


#
# GLOBALS
#

class Client:
    ORIGIN = 'origin'
    TARGET = 'target'
    LOCAL = 'local'


class SyncMode:
    """
    Sync Mode
    """

    DUMP_LOCAL = 'DUMP_LOCAL'
    DUMP_REMOTE = 'DUMP_REMOTE'
    IMPORT_LOCAL = 'IMPORT_LOCAL'
    IMPORT_REMOTE = 'IMPORT_REMOTE'
    RECEIVER = 'RECEIVER'
    SENDER = 'SENDER'
    PROXY = 'PROXY'
    SYNC_REMOTE = 'SYNC_REMOTE'
    SYNC_LOCAL = 'SYNC_LOCAL'

    @staticmethod
    def is_dump_local():
        """

        :return: boolean
        """
        return SyncMode.is_full_local() and SyncMode.is_same_host() and not SyncMode.is_sync_local()

    @staticmethod
    def is_dump_remote():
        """

        :return: boolean
        """
        return SyncMode.is_full_remote() and SyncMode.is_same_host() and \
               not SyncMode.is_sync_remote()

    @staticmethod
    def is_receiver():
        """

        :return: boolean
        """
        return 'host' in system.config[Client.ORIGIN] and not SyncMode.is_proxy() and \
               not SyncMode.is_sync_remote()

    @staticmethod
    def is_sender():
        """

        :return: boolean
        """
        return 'host' in system.config[Client.TARGET] and not SyncMode.is_proxy() and \
               not SyncMode.is_sync_remote()

    @staticmethod
    def is_proxy():
        """

        :return: boolean
        """
        return SyncMode.is_full_remote()

    @staticmethod
    def is_import_local():
        """

        :return: boolean
        """
        return system.config['import'] != '' and 'host' not in system.config[Client.TARGET]

    @staticmethod
    def is_import_remote():
        """

        :return: boolean
        """
        return system.config['import'] != '' and 'host' in system.config[Client.TARGET]

    @staticmethod
    def is_sync_local():
        """

        :return: boolean
        """
        return SyncMode.is_full_local() and SyncMode.is_same_host() and SyncMode.is_same_sync()

    @staticmethod
    def is_sync_remote():
        """

        :return: boolean
        """
        return SyncMode.is_full_remote() and SyncMode.is_same_host() and SyncMode.is_same_sync()

    @staticmethod
    def is_same_sync():
        """

        :return: boolean
        """
        return ((SyncMode.is_available_configuration('path') and
                 not SyncMode.is_same_configuration('path')) or
               (SyncMode.is_available_configuration('db') and
                not SyncMode.is_same_configuration('db')))

    @staticmethod
    def is_full_remote():
        """

        :return: boolean
        """
        return SyncMode.is_available_configuration('host')

    @staticmethod
    def is_full_local():
        """

        :return: boolean
        """
        return SyncMode.is_unavailable_configuration('host')

    @staticmethod
    def is_same_host():
        """

        :return: boolean
        """
        return SyncMode.is_same_configuration('host') and SyncMode.is_same_configuration('port')

    @staticmethod
    def is_available_configuration(key):
        """

        :return: boolean
        """
        return key in system.config[Client.ORIGIN] and key in system.config[Client.TARGET]

    @staticmethod
    def is_unavailable_configuration(key):
        """

        :return: boolean
        """
        return key not in system.config[Client.ORIGIN] and key not in system.config[Client.TARGET]

    @staticmethod
    def is_same_configuration(key):
        """

        :return: boolean
        """
        return (SyncMode.is_available_configuration(key) and
               system.config[Client.ORIGIN][key] == system.config[Client.TARGET][key]) or \
               SyncMode.is_unavailable_configuration(key)


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

    _modes = {
        SyncMode.RECEIVER: '(REMOTE ➔ LOCAL)',
        SyncMode.SENDER: '(LOCAL ➔ REMOTE)',
        SyncMode.PROXY: '(REMOTE ➔ LOCAL ➔ REMOTE)',
        SyncMode.DUMP_LOCAL: '(LOCAL, ONLY EXPORT)',
        SyncMode.DUMP_REMOTE: '(REMOTE, ONLY EXPORT)',
        SyncMode.IMPORT_LOCAL: '(REMOTE, ONLY IMPORT)',
        SyncMode.IMPORT_REMOTE: '(LOCAL, ONLY IMPORT)',
        SyncMode.SYNC_LOCAL: '(LOCAL ➔ LOCAL)',
        SyncMode.SYNC_REMOTE: '(REMOTE ➔ REMOTE)'
    }

    for _mode, _desc in _modes.items():
        if getattr(SyncMode, 'is_' + _mode.lower())():
            sync_mode = _mode
            _description = _desc

    if is_import():
        output.message(
            output.Subject.INFO,
            f'Import file {output.CliFormat.BLACK}{system.config["import"]}{output.CliFormat.ENDC}',
            True
        )

    system.config['is_same_client'] = SyncMode.is_same_host()

    output.message(
        output.Subject.INFO,
        f'Sync mode: {sync_mode} {output.CliFormat.BLACK}{_description}{output.CliFormat.ENDC}',
        True
    )

    check_for_protection()


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
    else:
        return False


def is_target_remote():
    """
    Check if target is remote client
    :return: Boolean
    """
    return sync_mode in (SyncMode.SENDER, SyncMode.PROXY, SyncMode.DUMP_REMOTE,
                         SyncMode.IMPORT_REMOTE, SyncMode.SYNC_REMOTE)


def is_origin_remote():
    """
    Check if origin is remote client
    :return: Boolean
    """
    return sync_mode in (SyncMode.RECEIVER, SyncMode.PROXY, SyncMode.DUMP_REMOTE,
                         SyncMode.IMPORT_REMOTE, SyncMode.SYNC_REMOTE)


def is_import():
    """
    Check if sync mode is import
    :return: Boolean
    """
    return sync_mode in (SyncMode.IMPORT_LOCAL, SyncMode.IMPORT_REMOTE)


def is_dump():
    """
    Check if sync mode is import
    :return: Boolean
    """
    return sync_mode in (SyncMode.DUMP_LOCAL, SyncMode.DUMP_REMOTE)


def run_command(command, client, force_output=False, allow_fail=False, skip_dry_run=False):
    """
    Run command depending on the given client
    :param command: String
    :param client: String
    :param force_output: Boolean
    :param allow_fail: Boolean
    :param skip_dry_run: Boolean
    :return:
    """
    if system.config['verbose']:
        output.message(
            output.host_to_subject(client),
            output.CliFormat.BLACK + command + output.CliFormat.ENDC,
            debug=True
        )

    if system.config['dry_run'] and skip_dry_run:
        return

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


def check_for_protection():
    """
    Check if the target system is protected
    :return: Boolean
    """
    if sync_mode in (SyncMode.RECEIVER, SyncMode.SENDER, SyncMode.PROXY, SyncMode.SYNC_LOCAL,
                     SyncMode.SYNC_REMOTE, SyncMode.IMPORT_LOCAL, SyncMode.IMPORT_REMOTE) and \
            'protect' in system.config[Client.TARGET]:
        _host = helper.get_ssh_host_name(Client.TARGET)
        sys.exit(output.message(output.Subject.ERROR,
                                f'The host {_host} is protected against the import of a database dump. Please '
                                'check synchronisation target or adjust the host configuration.', False))

