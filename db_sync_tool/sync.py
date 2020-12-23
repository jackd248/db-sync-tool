#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

from db_sync_tool.utility import system, helper, info
from db_sync_tool.database import process
from db_sync_tool.remote import transfer, client as remote_client


class Sync:
    """
    Synchronize a target database from an origin system
    """

    def __init__(self,
                 config_file=None,
                 verbose=False,
                 yes=False,
                 mute=False,
                 import_file=None,
                 dump_name=None,
                 keep_dump=None,
                 host_file=None,
                 config={}):
        """
        Initialization
        :param config_file:
        :param verbose:
        :param yes:
        :param mute:
        :param import_file:
        :param dump_name:
        :param keep_dump:
        :param host_file:
        :param config:
        """
        info.print_header(mute)
        system.check_args_options(
            config_file,
            verbose,
            yes,
            mute,
            import_file,
            dump_name,
            keep_dump,
            host_file
        )
        system.get_configuration(config)
        process.create_origin_database_dump()
        transfer.transfer_origin_database_dump()
        process.import_database_dump()
        helper.clean_up()
        remote_client.close_ssh_clients()
        info.print_footer()
