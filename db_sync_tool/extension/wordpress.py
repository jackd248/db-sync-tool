#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
from subprocess import check_output

from db_sync_tool.utility import mode, system, helper, output


def check_local_configuration(client):
    """
    Checking local Drupal database configuration
    :param client: String
    :return:
    """
    check_configuration(client)


def check_remote_configuration(client):
    """
    Checking remote Drupal database configuration
    :param client: String
    :return:
    """
    check_configuration(client)


def check_configuration(client):
    """
    Checking Drupal database configuration
    :param client: String
    :return:
    """
    _db_config = {
        'dbname': get_database_setting(client, 'DB_NAME', system.config['host'][client]['path']),
        'host': get_database_setting(client, 'DB_HOST', system.config['host'][client]['path']),
        'password': get_database_setting(client, 'DB_PASSWORD', system.config['host'][client]['path']),
        'port': get_database_setting(client, 'DB_PORT', system.config['host'][client]['path']) if get_database_setting(client, 'DB_PORT', system.config['host'][client]['path']) != '' else 3306,
        'user': get_database_setting(client, 'DB_USER', system.config['host'][client]['path']),
    }

    system.config['db'][client] = _db_config


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
        helper.get_command(client, 'sed') + f' -n "s/define( *\'{name}\', *\'\([^\']*\)\'.*/\\1/p" {file}',
        client,
        True
    ).replace('\n', '')

