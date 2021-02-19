#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

import argparse
import os
import sys
from collections import defaultdict

# Workaround for ModuleNotFoundError
sys.path.append(os.getcwd())
from db_sync_tool import sync
from db_sync_tool.utility import helper


def main(args=None):
    """
    Main entry point for the command line. Parse the arguments and call to the main process.
    :param args:
    :return:
    """
    if args is None:
        args = {}

    args = get_arguments(args)
    config = build_config(args)
    sync.Sync(
        config_file=args.config_file,
        verbose=args.verbose,
        yes=args.yes,
        mute=args.mute,
        import_file=args.import_file,
        dump_name=args.dump_name,
        keep_dump=args.keep_dump,
        host_file=args.host_file,
        clear=args.clear_database,
        config=config
    )


def get_arguments(args):
    """
    Parses and returns script arguments
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser(prog='db_sync_tool',
                                     description=f'A tool for automatic database synchronization from '
                                                 f'and to host systems.')
    parser.add_argument('-f', '--config-file',
                        help='Path to configuration file',
                        required=False,
                        type=str)
    parser.add_argument('-v', '--verbose',
                        help='Enable extended console output',
                        required=False,
                        action='store_true')
    parser.add_argument('-y', '--yes',
                        help='Skipping user confirmation for database import',
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
                        help='Skipping target import of the database dump and saving the available dump file in the '
                             'given directory',
                        required=False,
                        type=str)
    parser.add_argument('-o', '--host-file',
                        help='Using an additional hosts file for merging hosts information with the configuration file',
                        required=False,
                        type=str)
    parser.add_argument('-l', '--log-file',
                        help='File path for creating a additional log file',
                        required=False,
                        type=str)
    parser.add_argument('-cd', '--clear-database',
                        help='Dropping all tables before importing a new sync to get a clean database.',
                        required=False,
                        action='store_true')
    parser.add_argument('-t', '--type',
                        help='Defining the framework type [TYPO3, Symfony, Drupal, Wordpress]',
                        required=False,
                        type=str)
    parser.add_argument('-tp', '--target-path',
                        help='File path to target database credential file depending on the framework type',
                        required=False,
                        type=str)
    parser.add_argument('-tn', '--target-name',
                        help='Providing a name for the target system',
                        required=False,
                        type=str)
    parser.add_argument('-th', '--target-host',
                        help='SSH host to target system',
                        required=False,
                        type=str)
    parser.add_argument('-tu', '--target-user',
                        help='SSH user for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tpw', '--target-password',
                        help='SSH password for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tk', '--target-key',
                        help='File path to SSH key for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tpo', '--target-port',
                        help='SSH port for target system',
                        required=False,
                        type=int)
    parser.add_argument('-tdd', '--target-dump-dir',
                        help='Directory path for database dump file on target system',
                        required=False,
                        type=str)
    parser.add_argument('-tkd', '--target-keep-dumps',
                        help='Keep dump file count for target system',
                        required=False,
                        type=int)
    parser.add_argument('-tdn', '--target-db-name',
                        help='Database name for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tdh', '--target-db-host',
                        help='Database host for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tdu', '--target-db-user',
                        help='Database user for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tdpw', '--target-db-password',
                        help='Database password for target system',
                        required=False,
                        type=str)
    parser.add_argument('-tdpo', '--target-db-port',
                        help='Database port for target system',
                        required=False,
                        type=int)
    parser.add_argument('-tad', '--target-after-dump',
                        help='Additional dump file to insert after the regular database import',
                        required=False,
                        type=int)
    parser.add_argument('-op', '--origin-path',
                        help='File path to origin database credential file depending on the framework type',
                        required=False,
                        type=str)
    parser.add_argument('-on', '--origin-name',
                        help='Providing a name for the origin system',
                        required=False,
                        type=str)
    parser.add_argument('-oh', '--origin-host',
                        help='SSH host to origin system',
                        required=False,
                        type=str)
    parser.add_argument('-ou', '--origin-user',
                        help='SSH user for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-opw', '--origin-password',
                        help='SSH password for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-ok', '--origin-key',
                        help='File path to SSH key for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-opo', '--origin-port',
                        help='SSH port for origin system',
                        required=False,
                        type=int)
    parser.add_argument('-odd', '--origin-dump-dir',
                        help='Directory path for database dump file on origin system',
                        required=False,
                        type=str)
    parser.add_argument('-okd', '--origin-keep-dumps',
                        help='Keep dump file count for origin system',
                        required=False,
                        type=int)
    parser.add_argument('-odn', '--origin-db-name',
                        help='Database name for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-odh', '--origin-db-host',
                        help='Database host for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-odu', '--origin-db-user',
                        help='Database user for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-odpw', '--origin-db-password',
                        help='Database password for origin system',
                        required=False,
                        type=str)
    parser.add_argument('-odpo', '--origin-db-port',
                        help='Database port for origin system',
                        required=False,
                        type=int)

    return parser.parse_args(helper.dict_to_args(args))


def build_config(args):
    """
    Building an optional config
    :param args:
    :return:
    """
    config = defaultdict(lambda: defaultdict(dict))
    config['target'] = defaultdict(dict)
    config['origin'] = defaultdict(dict)

    if not args.type is None:
        config['type'] = args.type

    if not args.target_path is None:
        config['target']['path'] = args.target_path

    if not args.target_name is None:
        config['target']['name'] = args.target_name

    if not args.target_host is None:
        config['target']['host'] = args.target_host

    if not args.target_user is None:
        config['target']['user'] = args.target_user

    if not args.target_password is None:
        config['target']['password'] = args.target_password

    if not args.target_key is None:
        config['target']['ssh_key'] = args.target_key

    if not args.target_port is None:
        config['target']['port'] = args.target_port

    if not args.target_dump_dir is None:
        config['target']['dump_dir'] = args.target_dump_dir

    if not args.target_db_name is None:
        config['target']['db']['name'] = args.target_db_name

    if not args.target_db_host is None:
        config['target']['db']['host'] = args.target_db_host

    if not args.target_db_user is None:
        config['target']['db']['user'] = args.target_db_user

    if not args.target_db_password is None:
        config['target']['db']['password'] = args.target_db_password

    if not args.target_db_port is None:
        config['target']['db']['port'] = args.target_db_port

    if not args.target_after_dump is None:
        config['target']['after_dump'] = args.target_after_dump

    if not args.origin_path is None:
        config['origin']['path'] = args.origin_path

    if not args.origin_name is None:
        config['origin']['name'] = args.origin_name

    if not args.origin_host is None:
        config['origin']['host'] = args.origin_host

    if not args.origin_user is None:
        config['origin']['user'] = args.origin_user

    if not args.origin_password is None:
        config['origin']['password'] = args.origin_password

    if not args.origin_key is None:
        config['origin']['ssh_key'] = args.origin_key

    if not args.origin_port is None:
        config['origin']['port'] = args.origin_port

    if not args.origin_dump_dir is None:
        config['origin']['dump_dir'] = args.origin_dump_dir

    if not args.origin_db_name is None:
        config['origin']['db']['name'] = args.origin_db_name

    if not args.origin_db_host is None:
        config['origin']['db']['host'] = args.origin_db_host

    if not args.origin_db_user is None:
        config['origin']['db']['user'] = args.origin_db_user

    if not args.origin_db_password is None:
        config['origin']['db']['password'] = args.origin_db_password

    if not args.origin_db_port is None:
        config['origin']['db']['port'] = args.origin_db_port

    return config


if __name__ == "__main__":
    main()
