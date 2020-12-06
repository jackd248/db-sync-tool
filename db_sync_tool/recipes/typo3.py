#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import json

from db_sync_tool.utility import mode, system, helper


def check_configuration(client):
    """
    Checking remote TYPO3 database configuration
    :param client: String
    :return:
    """
    _path = system.config[client]['path']

    stdout = mode.run_command(
        helper.get_command(client, 'php') + ' -r "echo json_encode(include \'' + system.config[client][
            'path'] + '\');"',
        client,
        True
    )

    _db_config = parse_database_credentials(json.loads(stdout)['DB'])

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
