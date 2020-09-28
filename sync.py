#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from utility import system, database, helper, connect, info


def main():
    """
    Synchronize a target database from an origin system
    :return:
    """
    info.print_header()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Path to host file', required=False, type=str)
    parser.add_argument('-v', '--verbose', help='Enable extended console output', required=False, type=bool)
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



    system.check_args_options(parser.parse_args())
    system.check_configuration()
    database.create_origin_database_dump()
    connect.transfer_origin_database_dump()
    database.import_database_dump()
    helper.clean_up()
    connect.close_ssh_clients()

    info.print_footer()


#
# MAIN
#
if __name__ == "__main__":
    main()
