#!/usr/bin/python

import calendar, time, os, sys, datetime
from utility import output, connect, system, helper, mode

#
# GLOBALS
#
origin_database_dump_file_name = None


#
# CREATE ORIGIN DATABASE DUMP
#
def create_origin_database_dump():
    generate_database_dump_filename()

    output.message(
        output.get_subject().ORIGIN,
        'Creating database dump',
        True
    )
    mode.run_command(
        helper.get_command('origin', 'mysqldump') + ' ' + generate_mysql_credentials('origin') + ' ' +
        system.config['db']['origin'][
            'dbname'] + ' ' + generate_ignore_database_tables() + ' > ' + helper.get_origin_dump_dir() + origin_database_dump_file_name,
        mode.get_clients().ORIGIN
    )

    prepare_origin_database_dump()


def prepare_origin_database_dump():
    output.message(
        output.get_subject().ORIGIN,
        'Compressing database dump',
        True
    )
    mode.run_command(
        helper.get_command('origin',
                           'tar') + ' cfvz ' + helper.get_origin_dump_dir() + origin_database_dump_file_name + '.tar.gz -C ' + helper.get_origin_dump_dir() + ' ' + origin_database_dump_file_name,
        mode.get_clients().ORIGIN
    )


def generate_database_dump_filename():
    global origin_database_dump_file_name

    if system.option['dump_name'] == '':
        # _project-db_20-08-2020_12-37.sql
        _now = datetime.now()
        origin_database_dump_file_name = '_' + system.config['db']['origin']['dbname'] + '_' + now.strftime("%d-%m-%Y_%H-%M") + '.sql'
    else:
        origin_database_dump_file_name = system.option['dump_name'] + '.sql'


def generate_ignore_database_tables():
    _ignore_tables = []
    if 'ignore_table' in system.config['host']:
        for table in system.config['host']['ignore_table']:
            _ignore_tables.append('--ignore-table=' + system.config['db']['origin']['dbname'] + '.' + table)
        return ' '.join(_ignore_tables)


def generate_mysql_credentials(_target):
    _credentials = '-u\'' + system.config['db'][_target]['user'] + '\' -p\'' + system.config['db'][_target][
        'password'] + '\''
    if 'host' in system.config['db'][_target]:
        _credentials += ' -h\'' + system.config['db'][_target]['host'] + '\''
    if 'port' in system.config['db'][_target]:
        _credentials += ' -P\'' + str(system.config['db'][_target]['port']) + '\''
    return _credentials


#
# IMPORT DATABASE DUMP
#
def import_database_dump():
    if (not system.option['is_same_client']):
        prepare_target_database_dump()

    # @ToDo: Enable check_dump feature again
    #     if system.option['check_dump']:
    #         check_target_database_dump()

    if not system.option['keep_dump'] and not system.option['is_same_client']:
        output.message(
            output.get_subject().TARGET,
            'Importing database dump',
            True
        )

        mode.run_command(
            helper.get_command('target', 'mysql') + ' ' + generate_mysql_credentials('target') + ' ' +
            system.config['db']['target'][
                'dbname'] + ' < ' + helper.get_target_dump_dir() + origin_database_dump_file_name,
            mode.get_clients().TARGET
        )


def prepare_target_database_dump():
    output.message(output.get_subject().TARGET, 'Extracting database dump', True)
    mode.run_command(
        helper.get_command('target',
                           'tar') + ' xzf ' + helper.get_target_dump_dir() + origin_database_dump_file_name + '.tar.gz -C ' + helper.get_target_dump_dir(),
        mode.get_clients().TARGET
    )


# @ToDo: make this remote possible
def check_target_database_dump():
    with open(system.default_local_sync_path + origin_database_dump_file_name) as f:
        lines = f.readlines()
        if "-- Dump completed on" not in lines[-1]:
            sys.exit(output.message(output.get_subject().ERROR, 'Dump was not fully transferred', False))
