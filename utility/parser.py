#!/usr/bin/python

import system, mode, output, sys, connect


#
# GLOBALS
#
class framework:
    TYPO3 = 'TYPO3'
    SYMFONY = 'Symfony'


def get_framework():
    return framework


def get_database_configuration(client):
    system.config['db'] = {}

    # check framework type
    _base = ''
    if 'type' in system.config['host']:
        if system.config['host']['type'] == 'TYPO3':
            _base = framework.TYPO3
        elif system.config['host']['type'] == 'Symfony':
            _base = framework.SYMFONY
        else:
            sys.exit(
                output.message(
                    output.get_subject().ERROR,
                    'Framework type not supported',
                    False
                )
            )
    else:
        _base = framework.TYPO3

    if _base == framework.TYPO3:
        sys.path.append('./extension')
        from extension import typo3

        _parser = typo3

    elif _base == framework.SYMFONY:
        sys.path.append('./extension')
        from extension import symfony

        _parser = symfony

    if client == mode.get_clients().ORIGIN:
        output.message(
            output.get_subject().INFO,
            'Sync base: ' + _base,
            True
        )

        load_parser_origin(_parser)
    else:
        load_parser_target(_parser)


def load_parser_origin(parser):
    # check origin
    output.message(
        output.get_subject().ORIGIN,
        'Checking database configuration',
        True
    )
    if mode.is_origin_remote():
        connect.load_ssh_client_origin()
        parser.check_remote_configuration(mode.get_clients().ORIGIN)
    else:
        parser.check_local_configuration(mode.get_clients().ORIGIN)


def load_parser_target(parser):
    # check target
    output.message(
        output.get_subject().TARGET,
        'Checking database configuration',
        True
    )
    if mode.is_target_remote():
        connect.load_ssh_client_target()
        parser.check_remote_configuration(mode.get_clients().TARGET)
    else:
        parser.check_local_configuration(mode.get_clients().TARGET)
