#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
TYPO3 script
"""

import json

from db_sync_tool.utility import mode, system, helper


def check_configuration(client):
    """
    Checking remote TYPO3 database configuration
    :param client: String
    :return:
    """
    _path = system.config[client]['path']

    if 'LocalConfiguration' in _path:
        stdout = mode.run_command(
            helper.get_command(client, 'php') + ' -r "echo json_encode(include \'' +
            system.config[client][
                'path'] + '\');"',
            client,
            True
        )

        _db_config = parse_database_credentials(json.loads(stdout)['DB'])
    else:
        # Try to parse settings from AdditionalConfiguration.php file
        _db_config = {
            'name': get_database_setting(client, 'dbname', system.config[client]['path']),
            'host': get_database_setting(client, 'host', system.config[client]['path']),
            'password': get_database_setting(client, 'password', system.config[client]['path']),
            'port': get_database_setting(client, 'port', system.config[client]['path'])
            if get_database_setting(client, 'port',
                                    system.config[client]['path']) != '' else 3306,
            'user': get_database_setting(client, 'user', system.config[client]['path']),
        }

    system.config[client]['db'] = _db_config


def parse_database_credentials(db_credentials):
    """
    Parsing database credentials to needed format
    :param db_credentials: Dictionary
    :return: Dictionary
    """
    #
    # Distinguish between database config scheme of TYPO3 v8+ and TYPO3 v7-
    #
    if 'Connections' in db_credentials:
        _db_config = db_credentials['Connections']['Default']
        _db_config['name'] = _db_config['dbname']
    else:
        _db_config = db_credentials
        _db_config['user'] = _db_config['username']
        _db_config['name'] = _db_config['database']

    if 'port' not in _db_config:
        _db_config['port'] = 3306

    return _db_config


def get_database_setting(client, name, file):
    """
    Get database setting try to regex from AdditionalConfiguration
    sed -nE "s/'dbname'.*=>.*'(.*)'.*$/\1/p" /var/www/html/tests/files/www1/AdditionalConfiguration.php
    :param client: String
    :param name: String
    :param file: String
    :return:
    """
    return mode.run_command(
        helper.get_command(client, 'sed') +
        f' -nE "s/\'{name}\'.*=>.*\'(.*)\'.*$/\\1/p" {file}',
        client,
        True
    ).replace('\n', '').strip()
