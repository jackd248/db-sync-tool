#!/usr/bin/python

import argparse, sys, os, shutil
from utility import output, system, database, helper, connect

def main():

    print(output.get_bcolors().BLACK + '###############################' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '#' + output.get_bcolors().ENDC + '     TYPO3 Database Sync     ' + output.get_bcolors().BLACK + '#' + output.get_bcolors().ENDC)
    print(output.get_bcolors().BLACK + '###############################' + output.get_bcolors().ENDC)

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='Path to host file', required=False)
    parser.add_argument('-v', '--verbose', help='Enable extended console output', required=False)
    parser.add_argument('-kd', '--keepdump',
                        help='Skipping local import of the database dump and saving the available dump file in the given directory',
                        required=False)

    system.check_options(parser.parse_args())

    system.check_configuration()
    database.create_remote_database_dump()
    connect.get_remote_database_dump()
    database.import_database_dump()
    helper.clean_up()

    connect.ssh_client.close()
    output.message(
        output.get_subject().INFO,
        'Successfully synchronized databases',
        True
    )

#
# MAIN
#
if __name__ == "__main__":
    main()
