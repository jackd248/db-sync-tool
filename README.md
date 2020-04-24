# Database Sync Tool

Simple python script to synchronize a database from a remote to your local system.

Supported framework types:

- _TYPO3_
- _Symfony_

## Prerequisite

The script using python 2. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 
You can do this e.g. by the following command:

```bash
apt install -y python-pip
```

Additionally the python module [paramiko](https://github.com/paramiko/paramiko) is needed, to connect to the remote system. The module will be installed within the first script run or you can add the module using pip on your own:

```bash
pip install paramiko
```

## Install

While using the script within the PHP framework context, the script is available via [packagist.org](https://packagist.org/packages/kmi/db-sync-tool) using composer:

```bash
composer require kmi/db-sync-tool
```

## Configuration

The `host.json` contains important information about the remote and the local system. 
You need to specify the SSH credentials for the remote system and the path to the database credentials of both systems.

```bash
# Copy/edit host.json for TYPO3
cp dist/t3-db-sync.json.dist host.json

# Copy/edit host.json for Symfony
cp dist/sf-db-sync.json.dist host.json
```

Example structure of `host.json` for a Symfony system:
```json
{
  "name": "project",
  "type": "Symfony",
  "local": {
    "path": "/var/www/html/app/.env"
  },
  "remote": {
    "host": "ssh_host",
    "user": "ssh_user",
    "path": "/var/www/html/project/shared/.env"
  },
  "ignore_table": []
}
```

### Ignore tables

Often it is better to exclude some tables from the sql dump for performance reasons, e.g. caching tables. Specify them as comma separeted list in the `ignore_table` array.

### SSH key authentification

If you want to authenticate with a private ssh key instead of a password to the server (useful for CI/CD), you can a add the file path to the private key file in your `host.json`:

```json
{
  "ssh_key": "~/bob/.ssh/id_rsa"
}
```

### Console commands

The script using among other things the `php`, `mysql`, `mysqldump`, `grep` commands to synchronize the databases. Sometimes these commands are not available via the path variable, so you have to specify the full path to the source in the `host.json` depending on the target system:

```json
{
  "remote": {
    "console": {
      "php": "/usr/bin/php",
      "mysql": "/usr/bin/mysql",
      "mysqldump": "/usr/bin/mysqldump"
    }
  }
}
```

## Usage

```bash
# Run python script
python sync.py
```

```bash
# Options
-h, --help              Show help
-v, --verbose           Enable extended console output
-f, --file              Path to host file
-kd, --keepdump         Skipping local import of the database dump and saving the available dump file in the given directory
```

If you haven't declare a path to a SSH key, during the script execution you are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 


## FAQ

- First script run was aborted with the message `First install of additional pip modules completed. Please re-run the script.`
   
   Actually it is not possible to load the required pip modules and add them dynamically to the script execution. So you need to re-run the script again with the available dependencies.

- TYPO3 error message: `Unknown column '?' in 'field list'` 
   
   Sometimes your local environment differ from the remote system. So you maybe need to update the database schema either manually via the install tool or using the TYPO3 console by `typo3cms database:updateschema`