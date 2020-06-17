#!/usr/bin/python

import os, json, subprocess, re, sys
from subprocess import check_output
from utility import output, system, connect, helper, mode


def check_local_configuration(client):
    if os.path.isfile(system.config['host'][client]['path']) == False:
        sys.exit(output.message(output.get_subject().ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}

    _db_credentials = check_output(
        helper.get_command(client, 'grep') + ' -v "^#" ' + system.config['host'][client][
            'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
        stderr=subprocess.STDOUT,
        shell=True
    )

    _db_config = parse_database_credentials(_db_credentials)

    if system.option['verbose']:
        if client == mode.get_clients().TARGET:
            _subject = output.get_subject().TARGET
        else:
            _subject = output.get_subject().ORIGIN
        output.message(
            _subject,
            output.get_bcolors().BLACK + helper.get_command(client, 'grep') + ' -v "^#" ' +
            system.config['host'][client]['path'] + ' | ' + helper.get_command(client,
                                                                                 'grep') + ' DATABASE_URL' + output.get_bcolors().ENDC,
            True
        )

    system.config['db'][client] = _db_config


def check_remote_configuration(client):
    stdout = mode.run_command(
        helper.get_command(client, 'grep') + ' -v "^#" ' + system.config['host'][client][
            'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
        client
    )
    _db_credentials = stdout.readlines()[0]
    _db_config = parse_database_credentials(_db_credentials)
    system.config['db'][client] = _db_config


def parse_database_credentials(_db_credentials):
    _db_credentials = str(_db_credentials).replace('\\n\'','')
    # DATABASE_URL=mysql://db-user:1234@db-host:3306/db-name
    _db_credentials = re.findall(r"\/{2}(.+):(.+)@(.+):(\d+)\/(.+)", _db_credentials)[0]

    if len(_db_credentials) != 5:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Mismatch of expected database credentials',
                False
            )
        )

    _db_config = {
        'dbname': _db_credentials[4],
        'host': _db_credentials[2],
        'password': _db_credentials[1],
        'port': _db_credentials[3],
        'user': _db_credentials[0],
    }

    return _db_config
