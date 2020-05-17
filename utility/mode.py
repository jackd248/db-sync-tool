#!/usr/bin/python

import system, output

#
# GLOBALS
#
class sync_modes:
    RECEIVER = 'RECEIVER'
    SENDER = 'SENDER'
    PROXY = 'PROXY'

sync_mode = sync_modes.RECEIVER

def get_sync_modes():
    return sync_modes

def get_sync_mode():
    return sync_mode

def check_sync_mode():
    global sync_mode
    if 'host' in system.config['host']['origin']:
        sync_mode = sync_modes.RECEIVER
    if 'host' in system.config['host']['target']:
        sync_mode = sync_modes.SENDER
    if 'host' in system.config['host']['origin'] and 'host' in system.config['host']['target']:
        sync_mode = sync_modes.PROXY

    output.message(
        output.get_subject().INFO,
        'Sync mode: ' + sync_mode,
        True
    )

