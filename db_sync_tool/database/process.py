#!/usr/bin/env python3
# -*- coding: future_fstrings -*-

from db_sync_tool.utility import parser, mode, system, helper, output
from db_sync_tool.database import utility as database_utility


def create_origin_database_dump():
    """
    Creating the origin database dump file
    :return:
    """
    if not mode.is_import():
        parser.get_database_configuration(mode.Client.ORIGIN)
        database_utility.generate_database_dump_filename()
        helper.check_and_create_dump_dir(mode.Client.ORIGIN, helper.get_dump_dir(mode.Client.ORIGIN))

        _dump_file_path = helper.get_dump_dir(mode.Client.ORIGIN) + database_utility.database_dump_file_name

        output.message(
            output.Subject.ORIGIN,
            f'Creating database dump {output.CliFormat.BLACK}{_dump_file_path}{output.CliFormat.ENDC}',
            True
        )
        mode.run_command(
            helper.get_command('origin', 'mysqldump') + ' --no-tablespaces ' +
            database_utility. generate_mysql_credentials('origin') + ' ' +
            system.config['origin']['db']['name'] + ' ' +
            database_utility.generate_ignore_database_tables() +
            ' > ' + _dump_file_path,
            mode.Client.ORIGIN
        )

        database_utility.check_database_dump(mode.Client.ORIGIN, _dump_file_path)
        prepare_origin_database_dump()


def import_database_dump():
    """
    Importing the selected database dump file
    :return:
    """
    if not system.config['is_same_client'] and not mode.is_import():
        prepare_target_database_dump()

    if not system.config['keep_dump'] and not system.config['is_same_client']:
        output.message(
            output.Subject.TARGET,
            'Importing database dump',
            True
        )

        if not mode.is_import():
           _dump_path = helper.get_dump_dir(mode.Client.TARGET) + database_utility.database_dump_file_name
        else:
           _dump_path = system.config['import']

        if not system.config['yes']:
            _host_name = helper.get_ssh_host_name(mode.Client.TARGET, True) if mode.is_remote(mode.Client.TARGET) else 'local'

            helper.confirm(
                output.message(
                    output.Subject.TARGET,
                    f'Are you sure, you want to import the dump file into {_host_name} database?',
                    False
                ),
                True
            )

        database_utility.check_database_dump(mode.Client.TARGET, _dump_path)

        import_database_dump_file(mode.Client.TARGET, _dump_path)

    if 'after_dump' in system.config['target']:
        _after_dump = system.config['target']['after_dump']
        output.message(
            output.Subject.TARGET,
            f'Importing after_dump file {output.CliFormat.BLACK}{_after_dump}{output.CliFormat.ENDC}',
            True
        )

        import_database_dump_file(mode.Client.TARGET, _after_dump)


def import_database_dump_file(client, filepath):
    """
    Import a database dump file
    :param client: String
    :param filepath: String
    :return:
    """
    if helper.check_file_exists(client, filepath):
        mode.run_command(
            helper.get_command(client, 'mysql') + ' ' +
            database_utility.generate_mysql_credentials(client) + ' ' +
            system.config[client]['db']['name'] + ' < ' + filepath,
            client
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
            mode.Client.ORIGIN) + database_utility.database_dump_file_name + '.tar.gz -C ' + helper.get_dump_dir(
            mode.Client.ORIGIN) + ' ' + database_utility.database_dump_file_name + ' > /dev/null',
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
            mode.Client.TARGET) + database_utility.database_dump_file_name + '.tar.gz -C ' + helper.get_dump_dir(
            mode.Client.TARGET) + ' > /dev/null',
        mode.Client.TARGET
    )
