#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from db_sync_tool.utility import mode, system, output
from db_sync_tool.remote import client as remote_client, utility as remote_utility


class Framework:
    TYPO3 = 'TYPO3'
    SYMFONY = 'Symfony'
    DRUPAL = 'Drupal'
    WORDPRESS = 'Wordpress'


def get_database_configuration(client):
    """
    Getting database configuration of given client and defined sync base (framework type)
    :param client: String
    :return:
    """
    system.config['db'] = {}

    # check framework type
    _base = ''
    if 'type' in system.config['host']:
        _type = system.config['host']['type'].lower()
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

    load_parser(client, _parser)
    validate_database_credentials(client)


def load_parser(client, parser):
    """
    Loading parser and checking database configuration
    :param client:
    :param parser:
    :return:
    """
    output.message(
        output.host_to_subject(client),
        'Checking database configuration',
        True
    )
    if client == mode.Client.ORIGIN:
        if mode.is_origin_remote():
            remote_client.load_ssh_client_origin()
        else:
            remote_utility.run_before_script(client)
    else:
        if mode.is_target_remote():
            remote_client.load_ssh_client_target()
        else:
            remote_utility.run_before_script(client)

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
    _db_credential_keys = ['name', 'host', 'password', 'port', 'user']

    for _key in _db_credential_keys:
        if _key not in system.config['db'][client]:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Missing database credential "{_key}" for {client} client',
                    False
                )
            )
        if system.config['db'][client][_key] is None or system.config['db'][client][_key] == '':
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Missing database credential "{_key}" for {client} client',
                    False
                )
            )
