#!/usr/bin/python

import argparse, sys, os, shutil
from utility import output, system, database, helper, connect, info


def main():
    info.print_header()

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Path to host file', required=False)
    parser.add_argument('-v', '--verbose', help='Enable extended console output', required=False)
    parser.add_argument('-i', '--importfile', help='Import database from a specific file dump', required=False)
    parser.add_argument('-dn', '--dumpname', help='Set a specific dump file name (default is "_[dbname]_[date]")', required=False)
    parser.add_argument('-kd', '--keepdump',
                        help='Skipping target import of the database dump and saving the available dump file in the given directory',
                        required=False)

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
