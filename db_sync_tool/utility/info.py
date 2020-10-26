#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from db_sync_tool.utility import mode, system, output

# Check requirements
try:
    import json
    import os
except ImportError:
     sys.exit(
         output.message(
             output.Subject.ERROR,
             'Python requirements missing! Install with: pip3 install -r requirements.txt'
         )
     )

#
# FUNCTIONS
#

def print_header(args):
    """
    Printing console header
    :param args:
    :return:
    """
    _information = get_composer_information()

    if args.mute is False:
        print(output.CliFormat.BLACK + '############################################' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                                          #' + output.CliFormat.ENDC)
        print(
            output.CliFormat.BLACK + '#' + output.CliFormat.ENDC + '           DATABASE SYNC TOOL             ' + output.CliFormat.BLACK + '#' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                  v' + _information['version'] + '                  #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '# ' + _information['homepage'] + ' #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                                          #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '############################################' + output.CliFormat.ENDC)


def get_composer_information():
    """
    Reading local composer information
    :return: Dictionary
    """
    if os.path.isfile(os.path.dirname(os.path.realpath(__file__)) + '/../../composer.json'):
        with open(os.path.dirname(os.path.realpath(__file__)) + '/../../composer.json', 'r') as read_file:
            return json.load(read_file)
    else:
        sys.exit(
            output.message(
                output.Subject.ERROR,
                'Local composer information not found',
                False,
                True
            )
        )


def print_footer():
    """
    Printing console footer
    :return:
    """
    if not system.option['keep_dump'] and not system.option['is_same_client'] and not mode.is_import():
        _message = 'Successfully synchronized databases'
    elif mode.is_import():
        _message = 'Successfully imported database dump'
    else:
        _message = 'Successfully created database dump'

    output.message(
        output.Subject.INFO,
        _message,
        True,
        True
    )