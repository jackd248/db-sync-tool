#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from subprocess import check_output

from db_sync_tool.utility import mode, system, helper, output


def check_local_configuration(client):
    """
    Checking local TYPO3 database configuration
    :param client: String
    :return:
    """
    if not os.path.isfile(system.config['host'][client]['path']):
        sys.exit(
            output.message(
                output.Subject.ERROR,
                'Local database configuration not found',
                False
            )
        )

    #
    # https://stackoverflow.com/questions/7290357/how-to-read-a-php-array-from-php-file-in-python
    #
    _db_config = check_output(
        [helper.get_command(client, 'php'), '-r',
         'echo json_encode(include "' + system.config['host'][client]['path'] + '");']).decode()
    _db_config = parse_database_credentials(json.loads(_db_config)['DB'])

    if system.option['verbose']:
        if client == mode.Client.TARGET:
            _subject = output.Subject.TARGET
        else:
            _subject = output.Subject.ORIGIN
        output.message(_subject, output.CliFormat.BLACK + helper.get_command(client, 'php') + ' -r "echo json_encode(include "' +
                       system.config['host'][client]['path'] + '");"' + output.CliFormat.ENDC, True, False, True)

    system.config['db'][client] = _db_config


def check_remote_configuration(client):
    """
    Checking remote TYPO3 database configuration
    :param client: String
    :return:
    """
    stdout = mode.run_command(
        helper.get_command(client, 'php') + ' -r "echo json_encode(include \'' + system.config['host'][client][
            'path'] + '\');"',
        client
    )
    _db_config = stdout.readlines()[0]
    _db_config = parse_database_credentials(json.loads(_db_config)['DB'])

    system.config['db'][client] = _db_config


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
    else:
        _db_config = db_credentials
        _db_config['user'] = _db_config['username']
        _db_config['dbname'] = _db_config['database']

    return _db_config
