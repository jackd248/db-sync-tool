#!/usr/bin/python

import os
from utility import system, output, connect


#
# GLOBALS
#
class sync_modes:
    RECEIVER = 'RECEIVER'
    SENDER = 'SENDER'
    PROXY = 'PROXY'


class clients:
    ORIGIN = 'origin'
    TARGET = 'target'


sync_mode = sync_modes.RECEIVER


def get_sync_modes():
    return sync_modes


def get_sync_mode():
    return sync_mode


def check_sync_mode():
    global sync_mode

    if 'host' in system.config['host']['origin']:
        sync_mode = sync_modes.RECEIVER
        _description = output.get_bcolors().BLACK + '(REMOTE --> LOCAL)' + output.get_bcolors().ENDC
    if 'host' in system.config['host']['target']:
        sync_mode = sync_modes.SENDER
        _description = output.get_bcolors().BLACK + '(LOCAL --> REMOTE)' + output.get_bcolors().ENDC
    if 'host' in system.config['host']['origin'] and 'host' in system.config['host']['target']:
        sync_mode = sync_modes.PROXY
        _description = output.get_bcolors().BLACK + '(REMOTE --> LOCAL --> REMOTE)' + output.get_bcolors().ENDC

    output.message(
        output.get_subject().INFO,
        'Sync mode: ' + sync_mode + ' ' + _description,
        True
    )


def get_clients():
    return clients


def is_target_remote():
    return sync_mode == sync_modes.SENDER or sync_mode == sync_modes.PROXY


def is_origin_remote():
    return sync_mode == sync_modes.RECEIVER or sync_mode == sync_modes.PROXY


def run_command(command, client):
    if client == clients.ORIGIN:
        if system.option['verbose']:
            output.message(
                output.get_subject().ORIGIN,
                output.get_bcolors().BLACK + command + output.get_bcolors().ENDC,
                True
            )
        if is_origin_remote():
            return connect.run_ssh_command_origin(command)
        else:
            return os.system(command)
    elif client == clients.TARGET:
        if system.option['verbose']:
            output.message(
                output.get_subject().TARGET,
                output.get_bcolors().BLACK + command + output.get_bcolors().ENDC,
                True
            )
        if is_target_remote():
            return connect.run_ssh_command_target(command)
        else:
            return os.system(command)
