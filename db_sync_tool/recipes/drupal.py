#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
Drupal script
"""

import json
from db_sync_tool.utility import mode, system, helper, output


def check_configuration(client):
    """
    Checking Drupal database configuration with Drush
    :param client: String
    :return:
    """
    _path = system.config[client]['path']

    # Check Drush version
    _raw_version = mode.run_command(
        f'{helper.get_command(client, "drush")} status --fields=drush-version --format=string '
        f'-r {_path}',
        client,
        True
    )

    output.message(
        output.host_to_subject(client),
        f'Drush version: {_raw_version}',
        True
    )

    stdout = mode.run_command(
        f'{helper.get_command(client, "drush")} core-status --pipe '
        f'--fields=db-hostname,db-username,db-password,db-name,db-port '
        f'-r {_path}',
        client,
        True
    )

    _db_config = parse_database_credentials(json.loads(stdout))

    system.config[client]['db'] = _db_config


def parse_database_credentials(db_credentials):
    """
    Parsing database credentials to needed format
    :param db_credentials: Dictionary
    :return: Dictionary
    """
    _db_config = {
        'name': db_credentials['db-name'],
        'host': db_credentials['db-hostname'],
        'password': db_credentials['db-password'],
        'port': db_credentials['db-port'],
        'user': db_credentials['db-username'],
    }

    return _db_config
