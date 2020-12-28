#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import sys
import json
import os
from db_sync_tool.utility import mode, system, output
from db_sync_tool import info


def print_header(mute):
    """
    Printing console header
    :param mute: Boolean
    :return:
    """

    if mute is False:
        print(output.CliFormat.BLACK + '##############################################' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                                            #' + output.CliFormat.ENDC)
        print(
            output.CliFormat.BLACK + '#' + output.CliFormat.ENDC + '                DB SYNC TOOL                ' + output.CliFormat.BLACK + '#' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                   v' + info.__version__ + '                   #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#  ' + info.__homepage__ + '  #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '#                                            #' + output.CliFormat.ENDC)
        print(output.CliFormat.BLACK + '##############################################' + output.CliFormat.ENDC)


def print_footer():
    """
    Printing console footer
    :return:
    """
    if not system.config['keep_dump'] and not system.config['is_same_client'] and not mode.is_import():
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