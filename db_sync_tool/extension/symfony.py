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

    _db_credentials = check_output(
        helper.get_command(client, 'grep') + ' -v "^#" ' + system.config['host'][client][
            'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
        stderr=subprocess.STDOUT,
        shell=True
    ).decode()

    _db_config = parse_database_credentials(_db_credentials)

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
