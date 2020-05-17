#!/usr/bin/python

#
# SYSTEM UTILITY
#
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLACK = '\033[90m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class subject:
    INFO = bcolors.GREEN + '[INFO]' + bcolors.ENDC
    TARGET = bcolors.BLUE + '[TARGET]' + bcolors.ENDC
    ORIGIN = bcolors.PURPLE + '[ORIGIN]' + bcolors.ENDC
    ERROR = bcolors.RED + '[ERROR]' + bcolors.ENDC
    WARNING = bcolors.YELLOW + '[WARNING]' + bcolors.ENDC


def message(header, message, do_print):
    if do_print:
        print(header + ' ' + message)
    else:
        return header + ' ' + message

def get_bcolors():
    return bcolors

def get_subject():
    return subject