#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import datetime
from db_sync_tool.utility import parser, mode, system, helper, output

#
# GLOBALS
#

origin_database_dump_file_name = None

#
# FUNCTIONS
#

def create_origin_database_dump():
    """
    Creating the origin database dump file
    :return:
    """

    if not mode.is_import():
        parser.get_database_configuration(mode.Client.ORIGIN)
        generate_database_dump_filename()
        helper.check_and_create_dump_dir(mode.Client.ORIGIN, helper.get_dump_dir(mode.Client.ORIGIN))

        _dump_file_path = helper.get_dump_dir(mode.Client.ORIGIN) + origin_database_dump_file_name

        output.message(
            output.Subject.ORIGIN,
            'Creating database dump',
            True
        )
        mode.run_command(
            helper.get_command('origin', 'mysqldump') + ' --no-tablespaces ' + generate_mysql_credentials('origin') + ' ' +
            system.config['db']['origin'][
                'dbname'] + ' ' + generate_ignore_database_tables() + ' > ' + _dump_file_path,
            mode.Client.ORIGIN
        )

        check_database_dump(mode.Client.ORIGIN, _dump_file_path)
        prepare_origin_database_dump()


def generate_database_dump_filename():
    """
    Generate a database dump filename like "_[dbname]_[date].sql" or using the give filename
    :return:
    """
    global origin_database_dump_file_name

    if system.option['dump_name'] == '':
        # _project-db_20-08-2020_12-37.sql
        _now = datetime.datetime.now()
        origin_database_dump_file_name = '_' + system.config['db']['origin']['dbname'] + '_' + _now.strftime("%d-%m-%Y_%H-%M") + '.sql'
    else:
        origin_database_dump_file_name = system.option['dump_name'] + '.sql'


def generate_ignore_database_tables():
    """
    Generate the ignore tables options for the mysqldump command by the given table list
    :return: String
    """
    _ignore_tables = []
    if 'ignore_table' in system.config['host']:
        for table in system.config['host']['ignore_table']:
            _ignore_tables.append('--ignore-table=' + system.config['db']['origin']['dbname'] + '.' + table)
        return ' '.join(_ignore_tables)


def generate_mysql_credentials(client):
    """
    Generate the needed database credential information for the mysql command
    :param client: String
    :return:
    """
    _credentials = '-u\'' + system.config['db'][client]['user'] + '\' -p\'' + system.config['db'][client][
        'password'] + '\''
    if 'host' in system.config['db'][client]:
        _credentials += ' -h\'' + system.config['db'][client]['host'] + '\''
    if 'port' in system.config['db'][client]:
        _credentials += ' -P\'' + str(system.config['db'][client]['port']) + '\''
    return _credentials


#
# IMPORT DATABASE DUMP
#
def import_database_dump():
    """
    Importing the selected database dump file
    :return:
    """
    if (not system.option['is_same_client'] and not mode.is_import()):
        prepare_target_database_dump()

    if not system.option['keep_dump'] and not system.option['is_same_client']:
        output.message(
            output.Subject.TARGET,
            'Importing database dump',
            True
        )

        if not mode.is_import():
           _dump_path = helper.get_dump_dir(mode.Client.TARGET) + origin_database_dump_file_name
        else:
           _dump_path = system.option['import']

        check_database_dump(mode.Client.TARGET, _dump_path)
        mode.run_command(
            helper.get_command('target', 'mysql') + ' ' + generate_mysql_credentials('target') + ' ' +
            system.config['db']['target'][
                'dbname'] + ' < ' + _dump_path,
            mode.Client.TARGET
        )


def prepare_origin_database_dump():
    """
    Preparing the origin database dump file by compressing them as .tar.gz
    :return:
    """
    output.message(
        output.Subject.ORIGIN,
        'Compressing database dump',
        True
    )
    mode.run_command(
        helper.get_command(mode.Client.ORIGIN, 'tar') + ' cfvz ' + helper.get_dump_dir(
            mode.Client.ORIGIN) + origin_database_dump_file_name + '.tar.gz -C ' + helper.get_dump_dir(
            mode.Client.ORIGIN) + ' ' + origin_database_dump_file_name + ' > /dev/null',
        mode.Client.ORIGIN
    )


def prepare_target_database_dump():
    """
    Preparing the target database dump by the unpacked .tar.gz file
    :return:
    """
    output.message(output.Subject.TARGET, 'Extracting database dump', True)
    mode.run_command(
        helper.get_command('target', 'tar') + ' xzf ' + helper.get_dump_dir(
            mode.Client.TARGET) + origin_database_dump_file_name + '.tar.gz -C ' + helper.get_dump_dir(
            mode.Client.TARGET) + ' > /dev/null',
        mode.Client.TARGET
    )


def check_database_dump(client, filepath):
    """
    Checking the last line of the dump file if it contains "-- Dump completed on"
    :param client: String
    :param filepath: String
    :return:
    """

    if system.option['check_dump']:
        _line = mode.run_command(
            helper.get_command(client, 'tail') + ' -n 1 ' + filepath,
                client,
                True
            )

        if "-- Dump completed on" not in _line:
            sys.exit(output.message(output.Subject.ERROR, 'Dump file is corrupted', False))
