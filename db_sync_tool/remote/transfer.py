#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import sys
from db_sync_tool.utility import mode, system, helper, output
from db_sync_tool.database import utility as database_utility
from db_sync_tool.remote import utility, client


def transfer_origin_database_dump():
    """
    Transfer the origin database dump files
    :return:
    """
    if not mode.is_import():
        if mode.get_sync_mode() == mode.SyncMode.RECEIVER:
            get_origin_database_dump(helper.get_dump_dir(mode.Client.TARGET))
            system.check_target_configuration()
        elif mode.get_sync_mode() == mode.SyncMode.SENDER:
            system.check_target_configuration()
            put_origin_database_dump(helper.get_dump_dir(mode.Client.ORIGIN))
            utility.remove_origin_database_dump()
        elif mode.get_sync_mode() == mode.SyncMode.PROXY:
            helper.create_local_temporary_data_dir()
            get_origin_database_dump(system.default_local_sync_path)
            system.check_target_configuration()
            put_origin_database_dump(system.default_local_sync_path)
        elif system.config['is_same_client']:
            utility.remove_origin_database_dump(True)
    else:
        system.check_target_configuration()


def get_origin_database_dump(target_path):
    """
    Downloading the origin database dump files
    :param target_path: String
    :return:
    """
    sftp = client.ssh_client_origin.open_sftp()
    output.message(
        output.Subject.ORIGIN,
        'Downloading database dump',
        True
    )
    if mode.get_sync_mode() != mode.SyncMode.PROXY:
        helper.check_and_create_dump_dir(mode.Client.TARGET, target_path)

    #
    # ToDo: Download speed problems
    # https://github.com/paramiko/paramiko/issues/60
    #
    sftp.get(helper.get_dump_dir(mode.Client.ORIGIN) + database_utility.database_dump_file_name + '.tar.gz',
             target_path + database_utility.database_dump_file_name + '.tar.gz', download_status)
    sftp.close()
    if not system.config['mute']:
        print('')

    utility.remove_origin_database_dump()


def download_status(sent, size):
    """
    Printing the download status information
    :param sent: Float
    :param size: Float
    :return:
    """
    if not system.config['mute']:
        sent_mb = round(float(sent) / 1024 / 1024, 1)
        size = round(float(size) / 1024 / 1024, 1)
        sys.stdout.write(
            output.Subject.ORIGIN + output.CliFormat.BLACK + '[REMOTE]' + output.CliFormat.ENDC + " Status: {0} MB of {1} MB downloaded".
            format(sent_mb, size, ))
        sys.stdout.write('\r')


def put_origin_database_dump(origin_path):
    """
    Uploading the origin database dump file
    :param origin_path: String
    :return:
    """
    sftp = client.ssh_client_target.open_sftp()

    if (mode.get_sync_mode() == mode.SyncMode.PROXY):
        _subject = output.Subject.LOCAL
    else:
        _subject = output.Subject.ORIGIN

    output.message(
        _subject,
        'Uploading database dump',
        True
    )
    helper.check_and_create_dump_dir(mode.Client.TARGET, helper.get_dump_dir(mode.Client.TARGET))

    #
    # ToDo: Download speed problems
    # https://github.com/paramiko/paramiko/issues/60
    #
    sftp.put(origin_path + database_utility.database_dump_file_name + '.tar.gz',
             helper.get_dump_dir(mode.Client.TARGET) + database_utility.database_dump_file_name + '.tar.gz',
             upload_status)
    sftp.close()
    if not system.config['mute']:
        print('')


def upload_status(sent, size):
    """
    Printing the upload status information
    :param sent: Float
    :param size: Float
    :return:
    """
    if not system.config['mute']:
        sent_mb = round(float(sent) / 1024 / 1024, 1)
        size = round(float(size) / 1024 / 1024, 1)

        if (mode.get_sync_mode() == mode.SyncMode.PROXY):
            _subject = output.Subject.LOCAL
        else:
            _subject = output.Subject.ORIGIN + output.CliFormat.BLACK + '[LOCAL]' + output.CliFormat.ENDC

        sys.stdout.write(
            _subject + " Status: {0} MB of {1} MB uploaded".
            format(sent_mb, size, ))
        sys.stdout.write('\r')
