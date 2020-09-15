#!/usr/bin/python

import os, json, sys
from subprocess import check_output
from utility import output, system, connect, helper, mode

def check_local_configuration(client):
    if os.path.isfile(system.config['host'][client]['path']) == False:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Local database configuration not found',
                False
            )
        )

    #
    # https://stackoverflow.com/questions/7290357/how-to-read-a-php-array-from-php-file-in-python
    #
    _db_config = check_output(
        [helper.get_command(client, 'php'), '-r',
         'echo json_encode(include "' + system.config['host'][client]['path'] + '");']).decode()
    _db_config = parse_database_credentials(json.loads(_db_config)['DB'])

    if system.option['verbose']:
        if client == mode.get_clients().TARGET:
            _subject = output.get_subject().TARGET
        else:
            _subject = output.get_subject().ORIGIN
        output.message(_subject, output.get_bcolors().BLACK + helper.get_command(client,
                                                                                                    'php') + ' -r "echo json_encode(include "' +
                       system.config['host'][client]['path'] + '");"' + output.get_bcolors().ENDC, True)

    system.config['db'][client] = _db_config


def check_remote_configuration(client):
    stdout = mode.run_command(
        helper.get_command(client, 'php') + ' -r "echo json_encode(include \'' + system.config['host'][client][
            'path'] + '\');"',
        client
    )
    _db_config = stdout.readlines()[0]
    _db_config = parse_database_credentials(json.loads(_db_config)['DB'])

    system.config['db'][client] = _db_config


def parse_database_credentials(_db_credentials):
    #
    # Distinguish between database config scheme of TYPO3 v8+ and TYPO3 v7-
    #
    if 'Connections' in _db_credentials:
        _db_config = _db_credentials['Connections']['Default']
    else:
        _db_config = _db_credentials
        _db_config['user'] = _db_config['username']
        _db_config['dbname'] = _db_config['database']

    return _db_config
