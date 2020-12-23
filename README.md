# db sync tool

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/db_sync_tool-kmi)
![PyPI](https://img.shields.io/pypi/v/db_sync_tool-kmi)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/jackd248/db-sync-tool/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/jackd248/db-sync-tool/?branch=master)
[![Build Status](https://scrutinizer-ci.com/g/jackd248/db-sync-tool/badges/build.png?b=master)](https://scrutinizer-ci.com/g/jackd248/db-sync-tool/build-status/master)

Python script to synchronize a database from an origin to a target system with automatic database credential extraction depending on the selected framework.

Supported framework types:

- [TYPO3](https://typo3.org/) (>= v7.6)
- [Symfony](https://symfony.com/) (>= v2.8)
- [Drupal](https://www.drupal.org/) (>= v8.0)
- [Wordpress](https://wordpress.org) (>= v5.0)

## Prerequisite

The script needs python 3.5 or higher. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 

## Installation

<a name="install-pip"></a>
### pip
The library can be installed from [PyPI](https://pypi.org/):
```bash
$ pip3 install db-sync-tool-kmi
```

<a name="install-composer"></a>
### composer
While using the script within the PHP framework context, the script is available via [packagist.org](https://packagist.org/packages/kmi/db-sync-tool) using composer:

```bash
$ composer require kmi/db-sync-tool
```

Additionally install the python requirements via the following pip command:

````bash
$ pip3 install -r vendor/kmi/db-sync-tool/requirements.txt
````

## Configuration

You can configure the script with [shell arguments](#shell-arguments) or using a separate configuration file.

### Configuration File

The `config.json` contains important information about the origin and the target system. In dependence on the given configuration the synchronisation mode is implicitly selected.

Example structure of `config.json` for a Symfony system in receiver mode:
```json
{
  "type": "Symfony",
  "target": {
    "path": "/var/www/html/app/.env"
  },
  "origin": {
    "host": "ssh_host",
    "user": "ssh_user",
    "path": "/var/www/html/project/shared/.env"
  }
}
```

### Adjustments

It is possible to adjust the `config.json` [configuration](docs/CONFIG.md).

### Sync modes

The script provides seven different kinds of [synchronisation modes](docs/MODE.md).

- Receiver
- Sender
- Proxy
- Dump Local
- Dump Remote
- Import Local
- Import Remote

## Usage

### Command line

Run the python script via command line.

Installed via [pip](#install-pip):
```bash
$ python3 db_sync_tool
```

Installed via [composer](#install-composer):
```bash
$ python3 vendor/kmi/db-sync-tool/db_sync_tool
```

<a name="shell-arguments"></a>
#### Shell arguments

```bash
usage: db_sync_tool [-h] [-f CONFIG_FILE] [-v] [-y] [-m] [-i IMPORT_FILE]
                    [-dn DUMP_NAME] [-kd KEEP_DUMP] [-o HOST_FILE]
                    [-l LOG_FILE] [-t TYPE] [-tp TARGET_PATH]
                    [-tn TARGET_NAME] [-th TARGET_HOST] [-tu TARGET_USER]
                    [-tpw TARGET_PASSWORD] [-tk TARGET_KEY] [-tpo TARGET_PORT]
                    [-tdd TARGET_DUMP_DIR] [-tkd TARGET_KEEP_DUMPS]
                    [-tdn TARGET_DB_NAME] [-tdh TARGET_DB_HOST]
                    [-tdu TARGET_DB_USER] [-tdpw TARGET_DB_PASSWORD]
                    [-tdpo TARGET_DB_PORT] [-tad TARGET_AFTER_DUMP]
                    [-op ORIGIN_PATH] [-on ORIGIN_NAME] [-oh ORIGIN_HOST]
                    [-ou ORIGIN_USER] [-opw ORIGIN_PASSWORD] [-ok ORIGIN_KEY]
                    [-opo ORIGIN_PORT] [-odd ORIGIN_DUMP_DIR]
                    [-okd ORIGIN_KEEP_DUMPS] [-odn ORIGIN_DB_NAME]
                    [-odh ORIGIN_DB_HOST] [-odu ORIGIN_DB_USER]
                    [-odpw ORIGIN_DB_PASSWORD] [-odpo ORIGIN_DB_PORT]

A tool for automatic database synchronization from and to host systems.

optional arguments:
  -h, --help            show this help message and exit
  -f CONFIG_FILE, --config-file CONFIG_FILE
                        Path to configuration file
  -v, --verbose         Enable extended console output
  -y, --yes             Skipping user confirmation for database import
  -m, --mute            Mute console output
  -i IMPORT_FILE, --import-file IMPORT_FILE
                        Import database from a specific file dump
  -dn DUMP_NAME, --dump-name DUMP_NAME
                        Set a specific dump file name (default is
                        "_[dbname]_[date]")
  -kd KEEP_DUMP, --keep-dump KEEP_DUMP
                        Skipping target import of the database dump and saving
                        the available dump file in the given directory
  -o HOST_FILE, --host-file HOST_FILE
                        Using an additional hosts file for merging hosts
                        information with the configuration file
  -l LOG_FILE, --log-file LOG_FILE
                        File path for creating a additional log file
  -t TYPE, --type TYPE  Defining the framework type [TYPO3, Symfony, Drupal,
                        Wordpress]
  -tp TARGET_PATH, --target-path TARGET_PATH
                        File path to target database credential file depending
                        on the framework type
  -tn TARGET_NAME, --target-name TARGET_NAME
                        Providing a name for the target system
  -th TARGET_HOST, --target-host TARGET_HOST
                        SSH host to target system
  -tu TARGET_USER, --target-user TARGET_USER
                        SSH user for target system
  -tpw TARGET_PASSWORD, --target-password TARGET_PASSWORD
                        SSH password for target system
  -tk TARGET_KEY, --target-key TARGET_KEY
                        File path to SSH key for target system
  -tpo TARGET_PORT, --target-port TARGET_PORT
                        SSH port for target system
  -tdd TARGET_DUMP_DIR, --target-dump-dir TARGET_DUMP_DIR
                        Directory path for database dump file on target system
  -tkd TARGET_KEEP_DUMPS, --target-keep-dumps TARGET_KEEP_DUMPS
                        Keep dump file count for target system
  -tdn TARGET_DB_NAME, --target-db-name TARGET_DB_NAME
                        Database name for target system
  -tdh TARGET_DB_HOST, --target-db-host TARGET_DB_HOST
                        Database host for target system
  -tdu TARGET_DB_USER, --target-db-user TARGET_DB_USER
                        Database user for target system
  -tdpw TARGET_DB_PASSWORD, --target-db-password TARGET_DB_PASSWORD
                        Database password for target system
  -tdpo TARGET_DB_PORT, --target-db-port TARGET_DB_PORT
                        Database port for target system
  -tad TARGET_AFTER_DUMP, --target-after-dump TARGET_AFTER_DUMP
                        Additional dump file to insert after the regular
                        database import
  -op ORIGIN_PATH, --origin-path ORIGIN_PATH
                        File path to origin database credential file depending
                        on the framework type
  -on ORIGIN_NAME, --origin-name ORIGIN_NAME
                        Providing a name for the origin system
  -oh ORIGIN_HOST, --origin-host ORIGIN_HOST
                        SSH host to origin system
  -ou ORIGIN_USER, --origin-user ORIGIN_USER
                        SSH user for origin system
  -opw ORIGIN_PASSWORD, --origin-password ORIGIN_PASSWORD
                        SSH password for origin system
  -ok ORIGIN_KEY, --origin-key ORIGIN_KEY
                        File path to SSH key for origin system
  -opo ORIGIN_PORT, --origin-port ORIGIN_PORT
                        SSH port for origin system
  -odd ORIGIN_DUMP_DIR, --origin-dump-dir ORIGIN_DUMP_DIR
                        Directory path for database dump file on origin system
  -okd ORIGIN_KEEP_DUMPS, --origin-keep-dumps ORIGIN_KEEP_DUMPS
                        Keep dump file count for origin system
  -odn ORIGIN_DB_NAME, --origin-db-name ORIGIN_DB_NAME
                        Database name for origin system
  -odh ORIGIN_DB_HOST, --origin-db-host ORIGIN_DB_HOST
                        Database host for origin system
  -odu ORIGIN_DB_USER, --origin-db-user ORIGIN_DB_USER
                        Database user for origin system
  -odpw ORIGIN_DB_PASSWORD, --origin-db-password ORIGIN_DB_PASSWORD
                        Database password for origin system
  -odpo ORIGIN_DB_PORT, --origin-db-port ORIGIN_DB_PORT
                        Database port for origin system
```

If you haven't declare a path to a SSH key, during the script execution you are requested to enter the SSH password for the given user in the shell argument or the `config.json` to enable a SSH connection for the remote system. 

### Import

You can import the python package and use them inside your project:

```python
from db_sync_tool import sync

if __name__ == "__main__":
    sync.Sync(config={}, args*)
```

## Build

The packaging process of the python module is described on [python.org](https://packaging.python.org/tutorials/packaging-projects/).

## Tests

A docker container set up is available for testing purpose. See [here](tests/README.md).