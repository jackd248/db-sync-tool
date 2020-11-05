#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import sys
from subprocess import check_output

from db_sync_tool.utility import mode, system, helper, output


def check_local_configuration(client):
    """
    Checking local Symfony database configuration
    :param client: String
    :return:
    """
    if not os.path.isfile(system.config['host'][client]['path']):
        sys.exit(output.message(output.Subject.ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}
    # Check for symfony 2.8
    if 'parameters.yml' in system.config['host'][client]['path']:
        _db_config = {
            'dbname': get_database_parameter(client, 'database_name', system.config['host'][client]['path']),
            'host': get_database_parameter(client, 'database_host', system.config['host'][client]['path']),
            'password': get_database_parameter(client, 'database_password', system.config['host'][client]['path']),
            'port': get_database_parameter(client, 'database_port', system.config['host'][client]['path']),
            'user': get_database_parameter(client, 'database_user', system.config['host'][client]['path']),
        }
    # Using for symfony >=3.4
    else:
        _db_credentials = check_output(
            helper.get_command(client, 'grep') + ' -v "^#" ' + system.config['host'][client][
                'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
            stderr=subprocess.STDOUT,
            shell=True
        ).decode()

        _db_config = parse_database_credentials(_db_credentials)

    # ToDo: Clean this up
    if system.option['verbose']:
        if client == mode.Client.TARGET:
            _subject = output.Subject.TARGET
        else:
            _subject = output.Subject.ORIGIN
        output.message(
            _subject,
            output.CliFormat.BLACK + helper.get_command(client, 'grep') + ' -v "^#" ' +
            system.config['host'][client]['path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL' + output.CliFormat.ENDC,
            True,
            False,
            True
        )

    system.config['db'][client] = _db_config


def check_remote_configuration(client):
    """
    Checking remote Symfony database configuration
    :param client: String
    :return:
    """
    # Check for symfony 2.8
    if 'parameters.yml' in system.config['host'][client]['path']:
        _db_config = {
            'dbname': get_database_parameter(client, 'database_name', system.config['host'][client]['path']),
            'host': get_database_parameter(client, 'database_host', system.config['host'][client]['path']),
            'password': get_database_parameter(client, 'database_password', system.config['host'][client]['path']),
            'port': get_database_parameter(client, 'database_port', system.config['host'][client]['path']),
            'user': get_database_parameter(client, 'database_user', system.config['host'][client]['path']),
        }
    # Using for symfony >=3.4
    else:
        stdout = mode.run_command(
            helper.get_command(client, 'grep') + ' -v "^#" ' + system.config['host'][client][
                'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
            client
        )
        _db_credentials = stdout.readlines()[0]
        _db_config = parse_database_credentials(_db_credentials)

    system.config['db'][client] = _db_config


def parse_database_credentials(db_credentials):
    """
    Parsing database credentials to needed format
    :param client: Dictionary
    :return: Dictionary
    """
    db_credentials = str(db_credentials).replace('\\n\'','')
    # DATABASE_URL=mysql://db-user:1234@db-host:3306/db-name
    db_credentials = re.findall(r"\/{2}(.+):(.+)@(.+):(\d+)\/(.+)", db_credentials)[0]

    if len(db_credentials) != 5:
        sys.exit(
            output.message(
                output.Subject.ERROR,
                'Mismatch of expected database credentials',
                False
            )
        )

    _db_config = {
        'dbname': db_credentials[4],
        'host': db_credentials[2],
        'password': db_credentials[1],
        'port': db_credentials[3],
        'user': db_credentials[0],
    }

    return _db_config


def get_database_parameter(client, name, file):
    """
    Parsing a single database variable from the parameters.yml file
    hhttps://unix.stackexchange.com/questions/84922/extract-a-part-of-one-line-from-a-file-with-sed
    :param client: String
    :param name: String
    :param file: String
    :return:
    """
    return mode.run_command(
        helper.get_command(client, 'sed') + f' -n -e \'/{name}/ s/.*\\: *//p\' {file}',
        client,
        True
    ).replace('\n', '')