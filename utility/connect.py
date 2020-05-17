#!/usr/bin/python

import sys, output, system, database, helper, mode

#
# GLOBALS
#
ssh_client_origin = None
ssh_client_target = None


#
# SSH UTILITY
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

    if 'ssh_key' in system.config['host'][ssh]:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                key_filename=system.config['host'][ssh]['ssh_key'],
                                compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification for ' + system.config['host'][ssh]['host'] + ' failed',
                    False
                )
            )

        _authentication_method = 'using key'
    else:
        try:
            _ssh_client.connect(hostname=system.config['host'][ssh]['host'],
                                username=system.config['host'][ssh]['user'],
                                password=system.origin_ssh_password,
                                compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification for ' + system.config['host'][ssh]['host'] + ' failed',
                    False
                )
            )

        _authentication_method = 'using password'

    output.message(
        output.get_subject().ORIGIN,
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


def remove_origin_database_dump():
    output.message(
        output.get_subject().ORIGIN,
        'Cleaning up',
        True
    )
    sftp = ssh_client_origin.open_sftp()
    sftp.remove(helper.get_origin_dump_dir() + database.origin_database_dump_file_name)
    sftp.remove(helper.get_origin_dump_dir() + database.origin_database_dump_file_name + '.tar.gz')
    sftp.close()


#
# GET ORIGIN DATABASE DUMP
#
def get_origin_database_dump():
    system.create_local_temporary_data_dir()

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
             system.default_local_sync_path + database.origin_database_dump_file_name + '.tar.gz', download_status)
    sftp.close()
    print('')


def download_status(sent, size):
    sent_mb = round(float(sent) / 1024 / 1024, 1)
    size = round(float(size) / 1024 / 1024, 1)
    sys.stdout.write(
        output.get_subject().ORIGIN + output.get_bcolors().BLACK + '[REMOTE]' + output.get_bcolors().ENDC + " Status: {0} MB of {1} MB downloaded".
        format(sent_mb, size, ))
    sys.stdout.write('\r')
