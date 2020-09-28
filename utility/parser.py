#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from utility import output, system, mode, connect


#
# GLOBALS
#

class Framework:
    TYPO3 = 'TYPO3'
    SYMFONY = 'Symfony'

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

    sys.path.append('./extension')
    if _base == Framework.TYPO3:
        # Import TYPO3 parser
        from extension import typo3
        _parser = typo3

    elif _base == Framework.SYMFONY:
        # Import Symfony parser
        from extension import symfony
        _parser = symfony

    if client == mode.Client.ORIGIN:
        output.message(
            output.Subject.INFO,
            'Sync base: ' + _base,
            True
        )

        load_parser_origin(_parser)
    else:
        load_parser_target(_parser)


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
