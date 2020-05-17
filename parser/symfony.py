#!/usr/bin/python

import os, json, subprocess, re
from subprocess import check_output
from utility import output, system, connect, helper

def check_target_configuration():
    if os.path.isfile(system.config['host']['target']['path']) == False:
        sys.exit(output.message(output.get_subject().ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}

    output.message(
        output.get_subject().TARGET,
        'Checking database configuration',
        True
    )

    _database_credentials = check_output(
        helper.get_command('target','grep') + ' -v "^#" ' + system.config['host']['target']['path'] + ' | ' + helper.get_command('target','grep') + ' DATABASE_URL',
        stderr=subprocess.STDOUT,
        shell=True
    )

    _target_db_config = parse_database_credentials(_database_credentials)

    if system.option['verbose']:
        output.message(
            output.get_subject().TARGET,
            output.get_bcolors().BLACK + helper.get_command('target','grep') + ' -v "^#" ' + system.config['host']['target']['path'] + ' | ' + helper.get_command('target','grep') + ' DATABASE_URL' + output.get_bcolors().ENDC,
            True
        )

    system.config['db']['target'] = _target_db_config

def check_origin_configuration():
    output.message(output.get_subject().ORIGIN, 'Checking database configuration', True)
    stdout = connect.run_ssh_command(helper.get_command('origin','grep') + ' -v "^#" ' + system.config['host']['origin']['path'] + ' | ' + helper.get_command('origin','grep') + ' DATABASE_URL',)
    _database_credentials = stdout.readlines()[0]
    _origin_db_config = parse_database_credentials(_database_credentials)
    system.config['db']['origin'] = _origin_db_config

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

    _target_db_config = {
        'dbname': _database_credentials[4],
        'host': _database_credentials[2],
        'password': _database_credentials[1],
        'port': _database_credentials[3],
        'user': _database_credentials[0],
    }

    return _target_db_config