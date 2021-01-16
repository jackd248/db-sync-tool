#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import sys
from db_sync_tool.utility import mode, system, output, helper
from db_sync_tool.remote import client as remote_client, utility as remote_utility


class Framework:
    TYPO3 = 'TYPO3'
    SYMFONY = 'Symfony'
    DRUPAL = 'Drupal'
    WORDPRESS = 'Wordpress'
    MANUAL = 'Manual'


def get_database_configuration(client):
    """
    Getting database configuration of given client and defined sync base (framework type)
    :param client: String
    :return:
    """
    system.config['db'] = {}

    # check framework type
    _base = ''
    if 'type' in system.config:
        _type = system.config['type'].lower()
        if _type == 'typo3':
            # TYPO3 sync base
            _base = Framework.TYPO3
        elif _type == 'symfony':
            # Symfony sync base
            _base = Framework.SYMFONY
        elif _type == 'drupal':
            # Symfony sync base
            _base = Framework.DRUPAL
        elif _type == 'wordpress':
            # Symfony sync base
            _base = Framework.WORDPRESS
        else:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Framework type not supported: {_type}',
                    False
                )
            )
    elif 'db' in system.config['origin'] or 'db' in system.config['target']:
        _base = Framework.MANUAL
    else:
        # Default is TYPO3 sync base
        _base = Framework.TYPO3

    sys.path.append('../recipes')
    if _base == Framework.TYPO3:
        # Import TYPO3 parser
        from ..recipes import typo3
        _parser = typo3

    elif _base == Framework.SYMFONY:
        # Import Symfony parser
        from ..recipes import symfony
        _parser = symfony

    elif _base == Framework.DRUPAL:
        # Import Symfony parser
        from ..recipes import drupal
        _parser = drupal

    elif _base == Framework.WORDPRESS:
        # Import Symfony parser
        from ..recipes import wordpress
        _parser = wordpress

    if client == mode.Client.ORIGIN:
        output.message(
            output.Subject.INFO,
            'Sync base: ' + _base,
            True
        )

    if _base != Framework.MANUAL:
        load_parser(client, _parser)
    else:
        if client == mode.Client.ORIGIN and mode.is_origin_remote():
            remote_client.load_ssh_client_origin()
        elif client == mode.Client.TARGET and mode.is_target_remote():
            remote_client.load_ssh_client_target()

    validate_database_credentials(client)


def load_parser(client, parser):
    """
    Loading parser and checking database configuration
    :param client:
    :param parser:
    :return:
    """
    _path = system.config[client]['path']

    output.message(
        output.host_to_subject(client),
        f'Checking database configuration {output.CliFormat.BLACK}{_path}{output.CliFormat.ENDC}',
        True
    )
    if client == mode.Client.ORIGIN:
        if mode.is_origin_remote():
            remote_client.load_ssh_client_origin()
        else:
            helper.run_script(client, 'before')
    else:
        if mode.is_target_remote():
            remote_client.load_ssh_client_target()
        else:
            helper.run_script(client, 'before')

    # Check only if database configuration is a file
    if not helper.check_file_exists(client, _path) and _path[-1] is not '/':
        sys.exit(
            output.message(
                output.Subject.ERROR,
                f'Database configuration for {client} not found: {_path}',
                False
            )
        )
    parser.check_configuration(client)


def validate_database_credentials(client):
    """
    Validate the parsed database credentials
    :param client: String
    :return:
    """
    output.message(
        output.host_to_subject(client),
        'Validating database credentials',
        True
    )
    _db_credential_keys = ['name', 'host', 'password', 'user']

    for _key in _db_credential_keys:
        if _key not in system.config[client]['db']:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Missing database credential "{_key}" for {client} client',
                    False
                )
            )
        if system.config[client]['db'][_key] is None or system.config[client]['db'][_key] == '':
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Missing database credential "{_key}" for {client} client',
                    False
                )
            )
        else:
            output.message(
                output.host_to_subject(client),
                f'Database credential "{_key}" valid',
                verbose_only=True
            )
