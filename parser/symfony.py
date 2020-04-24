#!/usr/bin/python

import os, json, subprocess, re
from subprocess import check_output
from utility import output, system, connect, helper

def check_local_configuration():
    if os.path.isfile(system.config['host']['local']['path']) == False:
        sys.exit(output.message(output.get_subject().ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}

    output.message(
        output.get_subject().LOCAL,
        'Checking database configuration',
        True
    )

    _database_credentials = check_output(
        helper.get_command('local','grep') + ' -v "^#" ' + system.config['host']['local']['path'] + ' | ' + helper.get_command('local','grep') + ' DATABASE_URL',
        stderr=subprocess.STDOUT,
        shell=True
    )

    _local_db_config = parse_database_credentials(_database_credentials)

    if system.option['verbose']:
        output.message(
            output.get_subject().LOCAL,
            output.get_bcolors().BLACK + helper.get_command('local','grep') + ' -v "^#" ' + system.config['host']['local']['path'] + ' | ' + helper.get_command('local','grep') + ' DATABASE_URL' + output.get_bcolors().ENDC,
            True
        )

    system.config['db']['local'] = _local_db_config

def check_remote_configuration():
    output.message(output.get_subject().REMOTE, 'Checking database configuration', True)
    stdout = connect.run_ssh_command(helper.get_command('remote','grep') + ' -v "^#" ' + system.config['host']['remote']['path'] + ' | ' + helper.get_command('remote','grep') + ' DATABASE_URL',)
    _database_credentials = stdout.readlines()[0]
    _remote_db_config = parse_database_credentials(_database_credentials)
    system.config['db']['remote'] = _remote_db_config

def parse_database_credentials(_database_credentials):
    # DATABASE_URL=mysql://db-user:1234@db-host:3306/db-name
    _database_credentials = re.findall(r"\/{2}(.+):(.+)@(.+):(\d+)\/(.+)", _database_credentials)[0]

    if len(_database_credentials) != 5:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Mismatch of expected database credentials',
                False
            )
        )

    _local_db_config = {
        'dbname': _database_credentials[4],
        'host': _database_credentials[2],
        'password': _database_credentials[1],
        'port': _database_credentials[3],
        'user': _database_credentials[0],
    }

    return _local_db_config