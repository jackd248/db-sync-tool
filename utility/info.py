#!/usr/bin/python

import os, json, sys
from utility import output, system, mode


def print_header():
    _information = get_composer_information()

    print(output.get_bcolors().BLACK + '############################################' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '#                                          #' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '#' + output.get_bcolors().ENDC + '           DATABASE SYNC TOOL             ' + output.get_bcolors().BLACK + '#' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '#                  v' + _information['version'] + '                  #' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '# ' + _information['homepage'] + ' #' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '#                                          #' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '############################################' + output.get_bcolors().ENDC)


def get_composer_information():
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '/../composer.json'):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../composer.json', 'r') as read_file:
            return json.load(read_file)
    else:
        sys.exit(
            output.message(
                output.get_subject().ERROR,
                'Local composer information not found',
                False
            )
        )

def print_footer():
    if not system.option['keep_dump'] and not system.option['is_same_client']:
        output.message(
            output.get_subject().INFO,
            'Successfully synchronized databases',
            True
        )
    else:
        output.message(
            output.get_subject().INFO,
            'Successfully created database dump',
            True
        )