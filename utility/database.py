#!/usr/bin/python

import output, connect, calendar, time, system, os, sys


#
# GLOBALS
#
remote_database_dump_file_name = None

#
# CREATE REMOTE DATABASE DUMP
#
def create_remote_database_dump():
    generate_database_dump_filename()

    output.message(
        output.get_subject().REMOTE,
        'Creating database dump',
        True
    )
    connect.run_ssh_command('mysqldump ' + generate_mysql_credentials('remote') + ' ' + system.config['db']['remote'][
        'dbname'] + ' ' + generate_ignore_database_tables() + ' > ~/' + remote_database_dump_file_name)

    prepare_remote_database_dump()


def prepare_remote_database_dump():
    output.message(
        output.get_subject().REMOTE,
        'Compress database dump',
        True
    )
    connect.run_ssh_command('tar cfvz ~/' + remote_database_dump_file_name + '.tar.gz ' + remote_database_dump_file_name)


def generate_database_dump_filename():
    # _project_typo3_db_dump_1586780116.sql
    global remote_database_dump_file_name
    _timestamp = calendar.timegm(time.gmtime())
    remote_database_dump_file_name = '_' + system.config['host']['name'] + '_typo3_db_dump_' + str(_timestamp) + '.sql'


def generate_ignore_database_tables():
    _ignore_tables = []
    for table in system.config['ignore_table']:
        _ignore_tables.append('--ignore-table=' + system.config['db']['remote']['dbname'] + '.' + table)
    return ' '.join(_ignore_tables)


def generate_mysql_credentials(_target):
    _credentials = '-u\'' + system.config['db'][_target]['user'] + '\' -p\'' + system.config['db'][_target]['password'] + '\''
    if 'host' in system.config['db'][_target]:
        _credentials += ' -h\'' + system.config['db'][_target]['host'] + '\''
    if 'port' in system.config['db'][_target]:
        _credentials += ' -P\'' + str(system.config['db'][_target]['port']) + '\''
    return _credentials

#
# IMPORT DATABASE DUMP
#
def import_database_dump():
    prepare_local_database_dump()
    check_local_database_dump()

    if not system.option['keep_dump']:
        output.message(
            output.get_subject().LOCAL,
            'Importing database dump',
            True
        )

        if system.option['verbose']:
            output.message(
                output.get_subject().LOCAL,
                output.get_bcolors().BLACK + 'mysql ' + generate_mysql_credentials('local') + ' ' + system.config['db']['local'][
            'dbname'] + ' < ' + system.default_local_sync_path + remote_database_dump_file_name + output.get_bcolors().ENDC,
            True)

        os.system('mysql ' + generate_mysql_credentials('local') + ' ' + system.config['db']['local'][
            'dbname'] + ' < ' + system.default_local_sync_path + remote_database_dump_file_name)


def prepare_local_database_dump():
    output.message(output.get_subject().LOCAL, 'Extract database dump', True)
    if system.option['verbose']:
        output.message(
            output.get_subject().LOCAL,
            output.get_bcolors().BLACK + 'tar xzf ' + system.default_local_sync_path + remote_database_dump_file_name + '.tar.gz' + output.get_bcolors().ENDC,
            True
        )

    os.system('tar xzf ' + system.default_local_sync_path + remote_database_dump_file_name + '.tar.gz')

    os.system('mv ' + os.path.abspath(
        os.getcwd()) + '/' + remote_database_dump_file_name + ' ' + system.default_local_sync_path + remote_database_dump_file_name)


def check_local_database_dump():
    with open(system.default_local_sync_path + remote_database_dump_file_name) as f:
        lines = f.readlines()
        if "-- Dump completed on" not in lines[-1]:
            sys.exit(output.message(output.get_subject().ERROR, 'Dump was not fully transferred', False))