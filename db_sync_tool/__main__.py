#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from db_sync_tool import sync
from db_sync_tool.utility import helper


def main(args={}):
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :param args:
    :return:
    """
    args = get_arguments(args)
    sync.Sync(
        config_file=args.config_file,
        verbose=args.verbose,
        mute=args.mute,
        import_file=args.import_file,
        dump_name=args.dump_name,
        keep_dump=args.keep_dump,
        host_file=args.host_file
    )


def get_arguments(args):
    """
    Parses and returns script arguments
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config-file',
                        help='Path to configuration file',
                        required=False,
                        type=str)
    parser.add_argument('-v', '--verbose',
                        help='Enable extended console output',
                        required=False,
                        action='store_true')
    parser.add_argument('-m', '--mute',
                        help='Mute console output',
                        required=False,
                        action='store_true')
    parser.add_argument('-i', '--import-file',
                        help='Import database from a specific file dump',
                        required=False,
                        type=str)
    parser.add_argument('-dn', '--dump-name',
                        help='Set a specific dump file name (default is "_[dbname]_[date]")',
                        required=False,
                        type=str)
    parser.add_argument('-kd', '--keep-dump',
                        help='Skipping target import of the database dump and saving the available dump file in the given directory',
                        required=False,
                        type=str)
    parser.add_argument('-o', '--host-file',
                        help='Using an additional hosts file for merging hosts information with the configuration file',
                        required=False,
                        type=str)

    return parser.parse_args(helper.dict_to_args(args))


if __name__ == "__main__":
    main()
