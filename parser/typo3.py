#!/usr/bin/python

import os, json
from subprocess import check_output
from utility import output, system, connect

def check_local_configuration():
    if os.path.isfile(system.config['host']['local']['path']) == False:
        sys.exit(output.message(output.get_subject().ERROR, 'Local database configuration not found', False))

    system.config['db'] = {}
    #
    # https://stackoverflow.com/questions/7290357/how-to-read-a-php-array-from-php-file-in-python
    #
    _local_db_config = check_output(
        ['php', '-r', 'echo json_encode(include "' + system.config['host']['local']['path'] + '");'])
    _local_db_config = json.loads(_local_db_config)['DB']['Connections']['Default']
    output.message(output.get_subject().LOCAL, 'Checking database configuration', True)

    if system.option['verbose']:
            output.message(output.get_subject().LOCAL, output.get_bcolors().BLACK + 'php -r "echo json_encode(include "' + system.config['host']['local']['path'] + '");"' + output.get_bcolors().ENDC, True)

    system.config['db']['local'] = _local_db_config

def check_remote_configuration():
    output.message(output.get_subject().REMOTE, 'Checking database configuration', True)
    stdout = connect.run_ssh_command('php -r "echo json_encode(include \'' + system.config['host']['remote']['path'] + '\');"')
    _remote_db_config = stdout.readlines()[0]
    _remote_db_config = json.loads(_remote_db_config)['DB']['Connections']['Default']
    system.config['db']['remote'] = _remote_db_config