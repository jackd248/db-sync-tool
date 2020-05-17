#!/usr/bin/python

import os, json, sys
from subprocess import check_output
from utility import output, system, connect, helper, mode


def check_target_configuration():
    if os.path.isfile(system.config['host']['target']['path']) == False:
        sys.exit(output.message(output.get_subject().ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}
    #
    # https://stackoverflow.com/questions/7290357/how-to-read-a-php-array-from-php-file-in-python
    #
    _target_db_config = check_output(
        [helper.get_command('target', 'php'), '-r',
         'echo json_encode(include "' + system.config['host']['target']['path'] + '");'])
    _target_db_config = json.loads(_target_db_config)['DB']['Connections']['Default']
    output.message(output.get_subject().TARGET, 'Checking database configuration', True)

    if system.option['verbose']:
        output.message(output.get_subject().TARGET, output.get_bcolors().BLACK + helper.get_command('target',
                                                                                                    'php') + ' -r "echo json_encode(include "' +
                       system.config['host']['target']['path'] + '");"' + output.get_bcolors().ENDC, True)

    system.config['db']['target'] = _target_db_config


def check_origin_configuration():
    output.message(output.get_subject().ORIGIN, 'Checking database configuration', True)
    stdout = mode.run_command(
        helper.get_command('origin', 'php') + ' -r "echo json_encode(include \'' + system.config['host']['origin'][
            'path'] + '\');"',
        mode.get_clients().ORIGIN
    )
    _origin_db_config = stdout.readlines()[0]
    _origin_db_config = json.loads(_origin_db_config)['DB']['Connections']['Default']
    system.config['db']['origin'] = _origin_db_config
