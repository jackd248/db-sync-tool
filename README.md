# Database Sync Tool

Python script to synchronize a database from an origin to a target system with automatic database credential extraction depending on the selected framework.

Supported framework types:

- [TYPO3](https://typo3.org/) (>= v7.6)
- [Symfony](https://symfony.com/) (>= v2.8)
- [Drupal](https://www.drupal.org/) (>= v8.0)
- [Wordpress](https://wordpress.org) (>= v5.0)

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

### Command line

Run the python script:

```bash
$ python3 db_sync_tool
```

```bash
# Options
-h, --help              Show help
-v, --verbose           Enable extended console output
-f, --config-file       Path to config file
-i, --import-file       Import database from a specific file dump
-dn, --dump-name        Set a specific dump file name (default is "_[dbname]_[date]")
-kd, --keep-dump        Skipping target import of the database dump and saving the available dump file in the given directory
-o, --host-file         Using an additional hosts file for merging hosts information with the configuration file
```

If you haven't declare a path to a SSH key, during the script execution you are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 

### Import

You can import the python package and use them inside your project:

```python
from db_sync_tool import sync

if __name__ == "__main__":
    sync.Sync(args*, config)
```

## Build

The packaging process of the python module is described on [python.org](https://packaging.python.org/tutorials/packaging-projects/).

## Tests

A docker container set up is available for testing purpose. See [here](tests/README.md).