# Database Sync Tool

Python script to synchronize a database from an origin to a target system.

Supported framework types:

- TYPO3 (>= v7.6)
- Symfony (>= v3.4)

## Prerequisite

The script needs python 3.7 or higher. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 

## Installation

### pip
The library can be installed from [PyPI](https://pypi.org/):
```bash
$ pip3 install db-sync-tool-kmi
```

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

The `config.json` contains important information about the origin and the target system. In dependence on the given configuration the synchronisation mode is implicitly selected.

```bash
# Copy/edit host.json for TYPO3
$ cp docs/dist/t3-db-sync.json.dist config.json

# Copy/edit host.json for Symfony
$ cp docs/dist/sf-db-sync.json.dist config.json
```

Example structure of `config.json` for a Symfony system in receiver mode:
```json
{
  "name": "project",
  "type": "Symfony",
  "target": {
    "path": "/var/www/html/app/.env"
  },
  "origin": {
    "host": "ssh_host",
    "user": "ssh_user",
    "path": "/var/www/html/project/shared/.env"
  },
  "ignore_table": []
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

Run the python script:

```bash
$ python3 db_sync_tool/sync.py
```

```bash
# Options
-h, --help              Show help
-v, --verbose           Enable extended console output
-f, --file              Path to host file
-i, --importfile        Import database from a specific file dump
-dn, --dumpname         Set a specific dump file name (default is "_[dbname]_[date]")
-kd, --keepdump         Skipping target import of the database dump and saving the available dump file in the given directory
-o, --hosts             Using an additional hosts file for merging hosts information with the configuration file
```

If you haven't declare a path to a SSH key, during the script execution you are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 

## Build

The packaging process of the python module is described on [python.org](https://packaging.python.org/tutorials/packaging-projects/).

## Tests

A docker container set up is available for testing purpose. See [here](tests/README.md).