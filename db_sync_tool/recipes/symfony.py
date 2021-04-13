#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
Symfony script
"""

import re
import sys

from db_sync_tool.utility import mode, system, helper, output


def check_configuration(client):
    """
    Checking remote Symfony database configuration
    :param client: String
    :return:
    """
    _path = system.config[client]['path']

    # Check for symfony 2.8
    if 'parameters.yml' in _path:
        _db_config = {
            'name': get_database_parameter(client, 'database_name', _path),
            'host': get_database_parameter(client, 'database_host', _path),
            'password': get_database_parameter(client, 'database_password', _path),
            'port': get_database_parameter(client, 'database_port', _path),
            'user': get_database_parameter(client, 'database_user', _path),
        }
    # Using for symfony >=3.4
    else:
        stdout = mode.run_command(
            helper.get_command(client, 'grep') + ' -v "^#" ' + system.config[client][
                'path'] + ' | ' + helper.get_command(client, 'grep') + ' DATABASE_URL',
            client,
            True
        )
        _db_config = parse_database_credentials(stdout)

    system.config[client]['db'] = _db_config


def parse_database_credentials(db_credentials):
    """
    Parsing database credentials to needed format
    :param db_credentials: Dictionary
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
        'name': db_credentials[4],
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
