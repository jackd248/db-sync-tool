# Database Sync Tool

Python script to synchronize a database from an origin to a target system.

Supported framework types:

- TYPO3 (>= v7.6)
- Symfony (>= v3.4)

## Prerequisite

The script using python 3. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 
You can do this e.g. by the following command:

```bash
apt install -y python-pip
```

Additionally the python module [paramiko](https://github.com/paramiko/paramiko) is needed, to connect to the origin system. The module will be installed within the first script run or you can add the module using pip on your own:

```bash
pip install paramiko
```

## Install

While using the script within the PHP framework context, the script is available via [packagist.org](https://packagist.org/packages/kmi/db-sync-tool) using composer:

```bash
composer require kmi/db-sync-tool
```

## Configuration

The `host.json` contains important information about the origin and the target system. 
You need to specify the SSH credentials for the origin system and the path to the database credentials of both systems.

```bash
# Copy/edit host.json for TYPO3
cp dist/t3-db-sync.json.dist host.json

# Copy/edit host.json for Symfony
cp dist/sf-db-sync.json.dist host.json
```

Example structure of `host.json` for a Symfony system in receiver mode:
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

It is possible to adjust the `host.json` [configuration](documentation/CONFIG.md).

### Sync modes

The script provides five different kinds of [synchronisation modes](documentation/MODE.md).

- Receiver
- Sender
- Proxy
- Dump Local
- Dump Remote

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
-dn, --dumpname         Set a specific dump file name (default is "_[dbname]_[date]")
-kd, --keepdump         Skipping target import of the database dump and saving the available dump file in the given directory
```

If you haven't declare a path to a SSH key, during the script execution you are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 


## FAQ

- First script run was aborted with the message `First install of additional pip modules completed. Please re-run the script.`
   
   Actually it is not possible to load the required pip modules and add them dynamically to the script execution. So you need to re-run the script again with the available dependencies.

- TYPO3 error message: `Unknown column '?' in 'field list'` 
   
   Sometimes your local environment differ from the origin system. So you maybe need to update the database schema either manually via the install tool or using the TYPO3 console by `typo3cms database:updateschema`