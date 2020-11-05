#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from db_sync_tool.utility import mode, connect, system, output


#
# GLOBALS
#

class Framework:
    TYPO3 = 'TYPO3'
    SYMFONY = 'Symfony'
    DRUPAL = 'Drupal'
    WORDPRESS = 'Wordpress'

#
# FUNCTIONS
#
def get_framework():
    return Framework


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

    sys.path.append('../extension')
    if _base == Framework.TYPO3:
        # Import TYPO3 parser
        from ..extension import typo3
        _parser = typo3

    elif _base == Framework.SYMFONY:
        # Import Symfony parser
        from ..extension import symfony
        _parser = symfony

    elif _base == Framework.DRUPAL:
        # Import Symfony parser
        from ..extension import drupal
        _parser = drupal

    elif _base == Framework.WORDPRESS:
        # Import Symfony parser
        from ..extension import wordpress
        _parser = wordpress

    if client == mode.Client.ORIGIN:
        output.message(
            output.Subject.INFO,
            'Sync base: ' + _base,
            True
        )

        load_parser_origin(_parser)
    else:
        load_parser_target(_parser)

    validate_database_credentials(client)


def load_parser_origin(parser):
    """
    Loading origin parser
    :param parser:
    :return:
    """
    # @ToDo: Code duplication
    output.message(
        output.Subject.ORIGIN,
        'Checking database configuration',
        True
    )
    if mode.is_origin_remote():
        connect.load_ssh_client_origin()
        parser.check_remote_configuration(mode.Client.ORIGIN)
    else:
        connect.run_before_script(mode.Client.ORIGIN)
        parser.check_local_configuration(mode.Client.ORIGIN)


def load_parser_target(parser):
    """
    Loading target parser
    :param parser:
    :return:
    """
    # @ToDo: Code duplication
    output.message(
        output.Subject.TARGET,
        'Checking database configuration',
        True
    )
    if mode.is_target_remote():
        connect.load_ssh_client_target()
        parser.check_remote_configuration(mode.Client.TARGET)
    else:
        connect.run_before_script(mode.Client.TARGET)
        parser.check_local_configuration(mode.Client.TARGET)


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
    _db_credential_keys = ['dbname', 'host', 'password', 'port', 'user']

    for _key in _db_credential_keys:
        if system.config['db'][client][_key] is None or system.config['db'][client][_key] == '':
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    f'Missing database credential "{_key}" for {client} client',
                    False
                )
            )
