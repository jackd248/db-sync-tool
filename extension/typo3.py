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
         'echo json_encode(include "' + system.config['host'][client]['path'] + '");'])
    _db_config = json.loads(_db_config)['DB']['Connections']['Default']

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
    _db_config = json.loads(_db_config)['DB']['Connections']['Default']
    system.config['db'][client] = _db_config
