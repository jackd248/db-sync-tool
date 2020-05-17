#!/usr/bin/python

import output, connect, calendar, time, system, os, sys, helper, mode

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
    # _project_typo3_db_dump_1586780116.sql
    global origin_database_dump_file_name
    _timestamp = calendar.timegm(time.gmtime())
    origin_database_dump_file_name = '_' + system.config['host']['name'] + '_db_dump_' + str(_timestamp) + '.sql'


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
    prepare_target_database_dump()

    if system.option['check_dump']:
        check_target_database_dump()

    if not system.option['keep_dump']:
        output.message(
            output.get_subject().TARGET,
            'Importing database dump',
            True
        )

        mode.run_command(
            helper.get_command('target', 'mysql') + ' ' + generate_mysql_credentials('target') + ' ' +
            system.config['db']['target'][
                'dbname'] + ' < ' + system.default_local_sync_path + origin_database_dump_file_name,
            mode.get_clients().TARGET
        )


def prepare_target_database_dump():
    output.message(output.get_subject().TARGET, 'Extracting database dump', True)

    mode.run_command(
        helper.get_command('target',
                           'tar') + ' xzf ' + system.default_local_sync_path + origin_database_dump_file_name + '.tar.gz -C ' + system.default_local_sync_path,
        mode.get_clients().TARGET
    )


def check_target_database_dump():
    with open(system.default_local_sync_path + origin_database_dump_file_name) as f:
        lines = f.readlines()
        if "-- Dump completed on" not in lines[-1]:
            sys.exit(output.message(output.get_subject().ERROR, 'Dump was not fully transferred', False))
