#!/usr/bin/python

import output, os, json, sys


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
