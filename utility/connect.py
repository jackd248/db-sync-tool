#!/usr/bin/python

import sys, output, system, database

#
# GLOBALS
#
ssh_client = None

#
# SSH UTILITY
#
def get_ssh_client():
    global ssh_client
    ssh_client = system.paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(system.paramiko.AutoAddPolicy())

    if system.option['use_ssh_key']:
        try:
            ssh_client.connect(hostname=system.config['host']['remote']['host'],
                               username=system.config['host']['remote']['user'],
                               key_filename=system.config['host']['ssh_key'],
                               compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification failed',
                    False
                )
            )

        _authentication_method = 'using key'
    else:
        try:
            ssh_client.connect(hostname=system.config['host']['remote']['host'],
                               username=system.config['host']['remote']['user'],
                               password=system.remote_ssh_password,
                               compress=True)

        except system.paramiko.ssh_exception.AuthenticationException:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'SSH authentification failed',
                    False
                )
            )

        _authentication_method = 'using password'

    output.message(
        output.get_subject().REMOTE,
        'Successfully connect to ' + system.config['host']['remote']['user'] + '@' + system.config['host']['remote']['host'] + ' ' + _authentication_method,
        True
    )


def run_ssh_command(command):
    stdin, stdout, stderr = ssh_client.exec_command(command)
    exit_status = stdout.channel.recv_exit_status()

    if system.option['verbose']:
        output.message(output.get_subject().REMOTE, output.get_bcolors().BLACK + command + output.get_bcolors().ENDC, True)

    err = stderr.read().decode()
    if err and 0 != exit_status:
        sys.exit(output.message(output.get_subject().ERROR, err, False))
    elif err:
        output.message(output.get_subject().WARNING, err, True)

    return stdout


def download_status(sent, size):
    sent_mb = round(float(sent) / 1024 / 1024, 1)
    size = round(float(size) / 1024 / 1024, 1)
    sys.stdout.write(output.get_bcolors().PURPLE + "[REMOTE]" + output.get_bcolors().ENDC + " Status: {0} MB of {1} MB downloaded".
                     format(sent_mb, size, ))
    sys.stdout.write('\r')

def remove_remote_database_dump():
    output.message(
        output.get_subject().REMOTE,
        'Cleaning up',
        True
    )
    sftp = ssh_client.open_sftp()
    sftp.remove('/home/' + system.config['host']['remote']['user'] + '/' + database.remote_database_dump_file_name)
    sftp.remove('/home/' + system.config['host']['remote']['user'] + '/' + database.remote_database_dump_file_name + '.tar.gz')
    sftp.close()

#
# GET REMOTE DATABASE DUMP
#
def get_remote_database_dump():
    system.create_temporary_data_dir()

    sftp = ssh_client.open_sftp()
    output.message(
        output.get_subject().REMOTE,
        'Downloading database dump',
        True
        )
    #
    # ToDo: Download speed problems
    # https://github.com/paramiko/paramiko/issues/60
    #
    sftp.get('/home/' + system.config['host']['remote']['user'] + '/' + database.remote_database_dump_file_name + '.tar.gz',
             system.default_local_sync_path + database.remote_database_dump_file_name + '.tar.gz', download_status)
    sftp.close()
    print('')