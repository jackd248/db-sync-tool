#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

"""
Wordpress script
"""

from db_sync_tool.utility import mode, system, helper


def check_configuration(client):
    """
    Checking Drupal database configuration
    :param client: String
    :return:
    """
    _path = system.config[client]['path']

    _db_config = {
        'name': get_database_setting(client, 'DB_NAME', system.config[client]['path']),
        'host': get_database_setting(client, 'DB_HOST', system.config[client]['path']),
        'password': get_database_setting(client, 'DB_PASSWORD', system.config[client]['path']),
        'port': get_database_setting(client, 'DB_PORT', system.config[client]['path'])
        if get_database_setting(client, 'DB_PORT', system.config[client]['path']) != '' else 3306,
        'user': get_database_setting(client, 'DB_USER', system.config[client]['path']),
    }

    system.config[client]['db'] = helper.clean_db_config(_db_config)


def get_database_setting(client, name, file):
    """
    Parsing a single database variable from the wp-config.php file
    https://stackoverflow.com/questions/63493645/extract-database-name-from-a-wp-config-php-file
    :param client: String
    :param name: String
    :param file: String
    :return:
    """
    return mode.run_command(
        helper.get_command(client, 'sed') +
        f' -n "s/define( *\'{name}\', *\'\([^\']*\)\'.*/\\1/p" {file}',
        client,
        True
    ).replace('\n', '')
