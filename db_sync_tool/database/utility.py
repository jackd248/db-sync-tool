#!/usr/bin/env python3
# -*- coding: future_fstrings -*-


import sys
import datetime
from db_sync_tool.utility import mode, system, helper, output


database_dump_file_name = None


def run_database_command(client, command):
    """
    Run a database command using the "mysql -e" command
    :param client: String
    :param command: String database command
    :return:
    """
    return mode.run_command(
        helper.get_command(client, 'mysql') + ' ' + generate_mysql_credentials(client) + ' -e "' + command + '"',
        client, True)


def generate_database_dump_filename():
    """
    Generate a database dump filename like "_[name]_[date].sql" or using the give filename
    :return:
    """
    global database_dump_file_name

    if system.config['dump_name'] == '':
        # _project-db_20-08-2020_12-37.sql
        _now = datetime.datetime.now()
        database_dump_file_name = '_' + system.config['origin']['db']['name'] + '_' + _now.strftime(
            "%d-%m-%Y_%H-%M") + '.sql'
    else:
        database_dump_file_name = system.config['dump_name'] + '.sql'


def generate_ignore_database_tables():
    """
    Generate the ignore tables options for the mysqldump command by the given table list
    # ToDo: Too much conditional nesting
    :return: String
    """
    _ignore_tables = []
    if 'ignore_table' in system.config:
        for table in system.config['ignore_table']:
            if '*' in table:
                _wildcard_tables = get_database_tables_like('origin', table.replace('*', ''))
                if _wildcard_tables:
                    for wildcard_table in _wildcard_tables:
                        _ignore_tables = generate_ignore_database_table(_ignore_tables, wildcard_table)
            else:
                _ignore_tables = generate_ignore_database_table(_ignore_tables, table)
        return ' '.join(_ignore_tables)
    return ''


def generate_ignore_database_table(ignore_tables, table):
    """
    :param ignore_tables: Dictionary
    :param table: String
    :return:
    """
    ignore_tables.append('--ignore-table=' + system.config['origin']['db']['name'] + '.' + table)
    return ignore_tables


def get_database_tables_like(client, name):
    """
    Get database table names like the given name
    :param client: String
    :param name: String
    :return: Dictionary
    """
    _dbname = system.config[client]['db']['name']
    _tables = run_database_command(client, f'SHOW TABLES FROM {_dbname} LIKE \'%{name}%\';').strip()
    if _tables != '':
        return _tables.split('\n', 1)[1:]


def generate_mysql_credentials(client):
    """
    Generate the needed database credential information for the mysql command
    :param client: String
    :return:
    """
    _credentials = '-u\'' + system.config[client]['db']['user'] + '\' -p\'' + system.config[client]['db'][
        'password'] + '\''
    if 'host' in system.config[client]['db']:
        _credentials += ' -h\'' + system.config[client]['db']['host'] + '\''
    if 'port' in system.config[client]['db']:
        _credentials += ' -P\'' + str(system.config[client]['db']['port']) + '\''
    return _credentials


def check_database_dump(client, filepath):
    """
    Checking the last line of the dump file if it contains "-- Dump completed on"
    :param client: String
    :param filepath: String
    :return:
    """
    if system.config['check_dump']:
        _line = mode.run_command(
            helper.get_command(client, 'tail') + ' -n 1 ' + filepath,
            client,
            True
        )

        if "-- Dump completed on" not in _line:
            sys.exit(
                output.message(
                    output.Subject.ERROR,
                    'Dump file is corrupted',
                    do_print=False
                )
            )
        else:
            output.message(
                output.host_to_subject(client),
                'Dump file is valid',
                verbose_only=True
            )

