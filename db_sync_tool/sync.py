#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Konrad Michalik"
__copyright__ = "Copyright 2020"
__license__ = "MIT"
__version__ = "1.8.0"
__maintainer__ = "Konrad Michalik"
__email__ = "support@konradmichalik.eu"

import sys
import os
# Workaround for ModuleNotFoundError
sys.path.append(os.getcwd())
from db_sync_tool.utility import connect, system, helper, output, info, database

# Check Python version
assert sys.version_info >= (3, 7), sys.exit(output.message(output.Subject.ERROR, 'Python 3.7 or higher required'))

# Check requirements
try:
    import argparse
except ImportError:
     sys.exit(output.message(output.Subject.ERROR, 'Python requirements missing! Install with: pip3 install -r requirements.txt'))


class Sync:
    """
    Synchronize a target database from an origin system
    """

    _args = []

    def main(self, config={}):
        """
        Initialization
        :return:
        """
        self.get_arguments()
        info.print_header(self._args)
        system.check_args_options(self._args)
        system.get_configuration(config)
        database.create_origin_database_dump()
        connect.transfer_origin_database_dump()
        database.import_database_dump()
        helper.clean_up()
        connect.close_ssh_clients()
        info.print_footer()

    def get_arguments(self):
        """
        Parses and returns script arguments
        :param self:
        :return:
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', help='Path to host file', required=False, type=str)
        parser.add_argument('-v', '--verbose', help='Enable extended console output', required=False, action='store_true')
        parser.add_argument('-m', '--mute', help='Mute console output', required=False, action='store_true')
        parser.add_argument('-i', '--importfile', help='Import database from a specific file dump', required=False,
                            type=str)
        parser.add_argument('-dn', '--dumpname', help='Set a specific dump file name (default is "_[dbname]_[date]")',
                            required=False, type=str)
        parser.add_argument('-kd', '--keepdump',
                            help='Skipping target import of the database dump and saving the available dump file in the given directory',
                            required=False, type=str)
        parser.add_argument('-o', '--hosts',
                            help='Using an additional hosts file for merging hosts information with the configuration file',
                            required=False, type=str)
        self._args = parser.parse_args()


#
# MAIN
#
if __name__ == "__main__":
    sync = Sync()
    sync.main()
