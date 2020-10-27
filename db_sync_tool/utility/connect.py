#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import paramiko
import os
from db_sync_tool.utility import mode, system, helper, output, database


#
# GLOBALS
#

ssh_client_origin = None
ssh_client_target = None


#
# FUNCTIONS
#

def load_ssh_client_origin():
    """
    Loading the origin ssh client
    :return:
    """
    global ssh_client_origin
    ssh_client_origin = load_ssh_client(mode.Client.ORIGIN)
    run_before_script(mode.Client.ORIGIN)


def load_ssh_client_target():
    """
    Loading the target ssh client
    :return:
    """
    global ssh_client_target
    ssh_client_target = load_ssh_client(mode.Client.TARGET)
    run_before_script(mode.Client.TARGET)


def get_ssh_client_origin():
    """
    Returns the origin ssh client
    :return:
    """
    return ssh_client_origin


def get_ssh_client_target():
    """
    Returns the target ssh client
    :return:
    """
    return ssh_client_target


def load_ssh_client(ssh):
    """
    Initializing the given ssh client
    :param ssh: String
    :return:
    """
    _host_name = helper.get_ssh_host_name(ssh, True)
    _ssh_client = paramiko.SSHClient()
    _ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if 'port' in system.config['host'][ssh]:
        # Given SSH port
        _ssh_port = system.config['host'][ssh]['port']
    else:
        # Default SSH port
        _ssh_port = 22

    if 'ssh_key' in system.config['host'][ssh]:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                key_filename=system.config['host'][ssh]['ssh_key'],
                                port=_ssh_port,
                                compress=True)

        except paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'SSH authentication for {_host_name} failed',
                    False
                )
            )

        _authentication_method = f'{output.CliFormat.BLACK} - (authentication: key){output.CliFormat.ENDC}'
    else:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                port=_ssh_port,
                                password=system.config['host'][ssh]['password'],
                                compress=True)

        except paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'SSH authentication for {_host_name} failed',
                    False
                )
            )

        _authentication_method = f'{output.CliFormat.BLACK} - (authentication: password){output.CliFormat.ENDC}'

    output.message(
        output.host_to_subject(ssh),
        f'Successfully connect to {_host_name}{_authentication_method}',
        True
    )

    return _ssh_client


def run_before_script(client):
    """
    Executing before_script command
    :param client: String
    :return:
    """
    # Run before_script after successful connection
    if 'before_script' in system.config['host'][client]:
        output.message(
            output.host_to_subject(client),
            'Running before_script',
            True
        )
        mode.run_command(
            system.config['host'][client]['before_script'],
            client
        )


def run_after_script(client):
    """
    Executing after_script command
    :param client: String
    :return:
    """
    # Run after_script after successful connection
    if 'after_script' in system.config['host'][client]:
        output.message(
            output.host_to_subject(client),
            'Running after_script',
            True
        )
        mode.run_command(
            system.config['host'][client]['after_script'],
            client
        )


def close_ssh_clients():
    """
    Closing ssh client sessions
    :return:
    """
    run_after_script(mode.Client.ORIGIN)
    if not ssh_client_origin is None:
        ssh_client_origin.close()

    run_after_script(mode.Client.TARGET)
    if not ssh_client_target is None:
        ssh_client_target.close()


def run_ssh_command_by_client(client, command):
    """
    Running origin ssh command
    :param client: String
    :param command: String
    :return:
    """
    if client == mode.Client.ORIGIN:
        return run_ssh_command(command, ssh_client_origin)
    elif client == mode.Client.TARGET:
        return run_ssh_command(command, ssh_client_target)


def run_ssh_command_origin(command):
    """
    Running origin ssh command
    :param command: String
    :return:
    """
    return run_ssh_command(command, ssh_client_origin)


def run_ssh_command_target(command):
    """
    Running target ssh command
    :param command: String
    :return:
    """
    return run_ssh_command(command, ssh_client_target)


def run_ssh_command(command, ssh_client=ssh_client_origin):
    """
    Running ssh command
    :param command: String
    :param ssh_client:
    :return:
    """
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    err = stderr.read().decode()

    if err and 0 != exit_status:
        sys.exit(output.message(output.Subject.ERROR, err, False))
    elif err:
        output.message(output.Subject.WARNING, err, True)

    return stdout


#
# CLEAN UP
#
def remove_origin_database_dump(keep_compressed_file=False):
    """
    Removing the origin database dump files
    :param keep_compressed_file: Boolean
    :return:
    """
    output.message(
        output.Subject.ORIGIN,
        'Cleaning up',
        True
    )

    _file_path = helper.get_dump_dir(mode.Client.ORIGIN) + database.origin_database_dump_file_name
    if mode.is_origin_remote():
        sftp = ssh_client_origin.open_sftp()
        sftp.remove(_file_path)
        if not keep_compressed_file:
            sftp.remove(f'{_file_path}.tar.gz')
        sftp.close()
    else:
        os.remove(_file_path)
        if not keep_compressed_file:
            os.remove(f'{_file_path}.tar.gz')

    if keep_compressed_file:
        if 'keep_dumps' in system.config['host'][mode.Client.ORIGIN]:
            helper.clean_up_dump_dir(mode.Client.ORIGIN, helper.get_dump_dir(mode.Client.ORIGIN) + '*', system.config['host'][
                mode.Client.ORIGIN]['keep_dumps'])

        output.message(
            output.Subject.INFO,
            f'Database dump file is saved to: {_file_path}.tar.gz',
            True,
            True
        )


def remove_target_database_dump():
    """
    Removing the target database dump files
    :return:
    """
    _file_path = helper.get_dump_dir(mode.Client.TARGET) + database.origin_database_dump_file_name

    #
    # Move dump to specified directory
    #
    if system.option['keep_dump']:
        helper.create_local_temporary_data_dir()
        _keep_dump_path = system.default_local_sync_path + database.origin_database_dump_file_name
        mode.run_command(
            helper.get_command('target',
                               'cp') + ' ' + _file_path + ' ' + _keep_dump_path,
            mode.Client.TARGET
        )
        output.message(
            output.Subject.INFO,
            f'Database dump file is saved to: {_keep_dump_path}',
            True,
            True
        )

    #
    # Clean up
    #
    if (not system.option['is_same_client'] and not mode.is_import()):
        output.message(
            output.Subject.TARGET,
            'Cleaning up',
            True
        )

        if mode.is_target_remote():
            sftp = ssh_client_target.open_sftp()
            sftp.remove(_file_path)
            sftp.remove(f'{_file_path}.tar.gz')
            sftp.close()
        else:
            if os.path.isfile(_file_path):
                os.remove(_file_path)
            if os.path.isfile(f'{_file_path}.tar.gz'):
                os.remove(f'{_file_path}.tar.gz')


#
# TRANSFER ORIGIN DATABASE DUMP
#
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
            remove_origin_database_dump()
        elif mode.get_sync_mode() == mode.SyncMode.PROXY:
            helper.create_local_temporary_data_dir()
            get_origin_database_dump(system.default_local_sync_path)
            system.check_target_configuration()
            put_origin_database_dump(system.default_local_sync_path)
        elif system.option['is_same_client']:
            remove_origin_database_dump(True)
    else:
        system.check_target_configuration()


def get_origin_database_dump(target_path):
    """
    Downloading the origin database dump files
    :param target_path: String
    :return:
    """
    sftp = ssh_client_origin.open_sftp()
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
    sftp.get(helper.get_dump_dir(mode.Client.ORIGIN) + database.origin_database_dump_file_name + '.tar.gz',
             target_path + database.origin_database_dump_file_name + '.tar.gz', download_status)
    sftp.close()
    if not system.option['mute']:
        print('')

    remove_origin_database_dump()


def download_status(sent, size):
    """
    Printing the download status information
    :param sent: Float
    :param size: Float
    :return:
    """
    if not system.option['mute']:
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
    sftp = ssh_client_target.open_sftp()

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
    sftp.put(origin_path + database.origin_database_dump_file_name + '.tar.gz',
             helper.get_dump_dir(mode.Client.TARGET) + database.origin_database_dump_file_name + '.tar.gz', upload_status)
    sftp.close()
    if not system.option['mute']:
        print('')


def upload_status(sent, size):
    """
    Printing the upload status information
    :param sent: Float
    :param size: Float
    :return:
    """
    if not system.option['mute']:
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
