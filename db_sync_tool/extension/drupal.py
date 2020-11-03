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
    _os = helper.check_os(client).strip()
    _db_config = {
        'dbname': get_database_setting(client, 'database', system.config['host'][client]['path'], _os),
        'host': get_database_setting(client, 'host', system.config['host'][client]['path'], _os),
        'password': get_database_setting(client, 'password', system.config['host'][client]['path'], _os),
        'port': get_database_setting(client, 'port', system.config['host'][client]['path'], _os),
        'user': get_database_setting(client, 'username', system.config['host'][client]['path'], _os),
    }

    system.config['db'][client] = _db_config


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
        ).replace('"', '').replace('\n', '')
    else:
        return mode.run_command(
            helper.get_command(client, 'grep') + f' -Po "(?<=\'{name}\' => ).*(?=,)" {file}',
            client,
            True
        ).replace('"', '').replace('\n', '')

