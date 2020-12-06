#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

from db_sync_tool.utility import mode, system, helper


def check_configuration(client):
    """
    Checking Drupal database configuration
    :param client: String
    :return:
    """
    _os = helper.check_os(client).strip()
    _path = system.config[client]['path']

    _db_config = {
        'name': get_database_setting(client, 'database', _path, _os),
        'host': get_database_setting(client, 'host', _path, _os),
        'password': get_database_setting(client, 'password', _path, _os),
        'port': get_database_setting(client, 'port', _path, _os),
        'user': get_database_setting(client, 'username', _path, _os),
    }

    system.config[client]['db'] = _db_config


def get_database_setting(client, name, file, os):
    """
    Parsing a single database variable from the settings.php file
    :param client: String
    :param name: String
    :param file: String
    :param os: String
    :return:
    """
    if os == 'Darwin':
        return mode.run_command(
            helper.get_command(client, 'perl') + ' -nle "print $& while m{(?<=\'' + name + '\' => ).*(?=,)}g" ' + file + '| head -n 1',
            client,
            True
        ).replace('"', '').replace('\'', '').replace('\n', '')
    else:
        return mode.run_command(
            helper.get_command(client, 'grep') + f' -Po "(?<=\'{name}\' => ).*(?=,)" {file}',
            client,
            True
        ).replace('"', '').replace('\'', '').replace('\n', '')

