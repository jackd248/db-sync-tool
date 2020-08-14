#!/usr/bin/python

import sys, os
from utility import output, system, database, helper, mode

#
# GLOBALS
#

ssh_client_origin = None
ssh_client_target = None


#
# FUNCTIONS
#

def load_ssh_client_origin():
    global ssh_client_origin
    ssh_client_origin = load_ssh_client(mode.get_clients().ORIGIN)


def load_ssh_client_target():
    global ssh_client_target
    ssh_client_target = load_ssh_client(mode.get_clients().TARGET)


def get_ssh_client_origin():
    return ssh_client_origin


def get_ssh_client_target():
    return ssh_client_target


def load_ssh_client(ssh):
    _ssh_client = system.paramiko.SSHClient()
    _ssh_client.set_missing_host_key_policy(system.paramiko.AutoAddPolicy())

    if 'port' in system.config['host'][ssh]:
        _ssh_port = system.config['host'][ssh]['port']
    else:
        _ssh_port = 22

    if 'ssh_key' in system.config['host'][ssh]:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                key_filename=system.config['host'][ssh]['ssh_key'],
                                port=_ssh_port,
                                compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification for ' + system.config['host'][ssh]['host'] + ' failed',
                    False
                )
            )

        _authentication_method = '(authentication: key)'
    else:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                port=_ssh_port,
                                password=system.option['ssh_password'][ssh],
                                compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification for ' + system.config['host'][ssh]['host'] + ' failed',
                    False
                )
            )

        _authentication_method = '(authentication: password)'

    output.message(
        output.client_to_subject(ssh),
        'Successfully connect to ' + system.config['host'][ssh]['user'] + '@' + system.config['host'][ssh][
            'host'] + ' ' + _authentication_method,
        True
    )

    return _ssh_client


def close_ssh_clients():
    if not ssh_client_origin is None:
        ssh_client_origin.close()
    if not ssh_client_target is None:
        ssh_client_target.close()


def run_ssh_command_origin(command):
    return run_ssh_command(command, ssh_client_origin)


def run_ssh_command_target(command):
    return run_ssh_command(command, ssh_client_target)


def run_ssh_command(command, ssh_client=ssh_client_origin):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    err = stderr.read().decode()

    if err and 0 != exit_status:
        sys.exit(output.message(output.get_subject().ERROR, err, False))
    elif err:
        output.message(output.get_subject().WARNING, err, True)

    return stdout


#
# CLEAN UP
#
def remove_origin_database_dump(keep_compressed_file = False):
    output.message(
        output.get_subject().ORIGIN,
        'Cleaning up',
        True
    )

    _file_path = helper.get_origin_dump_dir() + database.origin_database_dump_file_name
    if mode.is_origin_remote():
        sftp = ssh_client_origin.open_sftp()
        sftp.remove(_file_path)
        if not keep_compressed_file:
            sftp.remove(_file_path + '.tar.gz')
        sftp.close()
    else:
        os.remove(_file_path)
        if not keep_compressed_file:
            os.remove(_file_path + '.tar.gz')

    if keep_compressed_file:
        output.message(
            output.get_subject().INFO,
            'Database dump file is saved to: ' + _file_path+ '.tar.gz',
            True
        )


def remove_target_database_dump():
    _file_path = helper.get_target_dump_dir() + database.origin_database_dump_file_name

    #
    # Move dump to specified directory
    #
    if system.option['keep_dump']:
        helper.create_local_temporary_data_dir()
        _keep_dump_path = system.default_local_sync_path +  database.origin_database_dump_file_name
        mode.run_command(
            helper.get_command('target',
                               'cp') + ' ' + _file_path + ' ' + _keep_dump_path,
            mode.get_clients().TARGET
        )
        output.message(
            output.get_subject().INFO,
            'Database dump file is saved to: ' + _keep_dump_path,
            True
        )

    #
    # Clean up
    #
    if (not system.option['is_same_client'] and not mode.is_import()):
        output.message(
            output.get_subject().TARGET,
            'Cleaning up',
            True
        )

        if mode.is_target_remote():
            sftp = ssh_client_target.open_sftp()
            sftp.remove(_file_path)
            sftp.remove(_file_path + '.tar.gz')
            sftp.close()
        else:
            if os.path.isfile(_file_path):
                os.remove(_file_path)
            if os.path.isfile(_file_path + '.tar.gz'):
                os.remove(_file_path + '.tar.gz')


#
# TRANSFER ORIGIN DATABASE DUMP
#
def transfer_origin_database_dump():
    if not mode.is_import():
        if mode.get_sync_mode() == mode.get_sync_modes().RECEIVER:
            get_origin_database_dump(helper.get_target_dump_dir())
            system.check_target_configuration()
        elif mode.get_sync_mode() == mode.get_sync_modes().SENDER:
            system.check_target_configuration()
            put_origin_database_dump(helper.get_origin_dump_dir())
            remove_origin_database_dump()
        elif mode.get_sync_mode() == mode.get_sync_modes().PROXY:
            helper.create_local_temporary_data_dir()
            get_origin_database_dump(system.default_local_sync_path)
            system.check_target_configuration()
            put_origin_database_dump(system.default_local_sync_path)
        elif system.option['is_same_client']:
            remove_origin_database_dump(True)
    else:
        system.check_target_configuration()


def get_origin_database_dump(target_path):
    sftp = ssh_client_origin.open_sftp()
    output.message(
        output.get_subject().ORIGIN,
        'Downloading database dump',
        True
    )

    #
    # ToDo: Download speed problems
    # https://github.com/paramiko/paramiko/issues/60
    #
    sftp.get(helper.get_origin_dump_dir() + database.origin_database_dump_file_name + '.tar.gz',
             target_path + database.origin_database_dump_file_name + '.tar.gz', download_status)
    sftp.close()
    print('')

    remove_origin_database_dump()


def download_status(sent, size):
    sent_mb = round(float(sent) / 1024 / 1024, 1)
    size = round(float(size) / 1024 / 1024, 1)
    sys.stdout.write(
        output.get_subject().ORIGIN + output.get_bcolors().BLACK + '[REMOTE]' + output.get_bcolors().ENDC + " Status: {0} MB of {1} MB downloaded".
        format(sent_mb, size, ))
    sys.stdout.write('\r')


def put_origin_database_dump(origin_path):
    sftp = ssh_client_target.open_sftp()

    if (mode.get_sync_mode() == mode.get_sync_modes().PROXY):
        _subject = output.get_subject().LOCAL
    else:
        _subject = output.get_subject().ORIGIN

    output.message(
        _subject,
        'Uploading database dump',
        True
    )

    #
    # ToDo: Download speed problems
    # https://github.com/paramiko/paramiko/issues/60
    #
    sftp.put(origin_path + database.origin_database_dump_file_name + '.tar.gz',
             helper.get_target_dump_dir() + database.origin_database_dump_file_name + '.tar.gz', upload_status)
    sftp.close()
    print('')


def upload_status(sent, size):
    sent_mb = round(float(sent) / 1024 / 1024, 1)
    size = round(float(size) / 1024 / 1024, 1)

    if (mode.get_sync_mode() == mode.get_sync_modes().PROXY):
        _subject = output.get_subject().LOCAL
    else:
        _subject = output.get_subject().ORIGIN + output.get_bcolors().BLACK + '[LOCAL]' + output.get_bcolors().ENDC

    sys.stdout.write(
        _subject + " Status: {0} MB of {1} MB uploaded".
        format(sent_mb, size, ))
    sys.stdout.write('\r')
