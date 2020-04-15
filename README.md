# TYPO3 Database Sync

Simple python script to synchronize a TYPO3 database from a remote to your local system.

## Prerequisite

The script using python 2. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 
You can do this e.g. by the following command:

```bash
apt install -y python-pip
```

## Install

While using the script within the TYPO3 context, the script is available via [packagist.org](https://packagist.org/packages/kmi/t3-db-sync) using composer:

```bash
composer require kmi/t3-db-sync
```

## Configuration

The `host.json` contains important information about the remote and the local system. 
You need to specify the SSH credentials for the remote system and the path to the `LocalConfiguration.php` of both systems.

```bash
# Copy/edit host.json
mv host.json.dist host.json
```

Example structure of `host.json`:
```json
{
  "name": "project",
  "local": {
    "path": "/var/www/html/htdocs/typo3/web/typo3conf/LocalConfiguration.php"
  },
  "remote": {
    "host": "ssh_host",
    "user": "ssh_user",
    "path": "/var/www/html/project/shared/typo3conf/LocalConfiguration.php"
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
-c, --config            Path to host file
-kd, --keepdump         Skipping local import of the database dump and saving the available dump file in the given directory
```

You are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 

### Ignore tables

Often it is better to exclude some tables from the sql dump for performance reasons, e.g. caching tables. There is a default stack of ignored tables within the script, but you can specify them in your `host.json`. The following tables are the default setting:

```json
{
  "ignore_table": [
    "sys_domain",
    "cf_cache_hash",
    "cf_cache_hash_tags",
    "cf_cache_news_category",
    "cf_cache_news_category_tags",
    "cf_cache_pages",
    "cf_cache_pagesection",
    "cf_cache_pagesection_tags",
    "cf_cache_pages_tags",
    "cf_cache_rootline",
    "cf_cache_rootline_tags",
    "cf_extbase_datamapfactory_datamap",
    "cf_extbase_datamapfactory_datamap_tags",
    "cf_extbase_object",
    "cf_extbase_object_tags",
    "cf_extbase_reflection",
    "cf_extbase_reflection_tags"
  ]
}
```

## FAQ

- First script run was aborted with the message `First install of additional pip modules completed. Please re-run the script.`
   
   Actually it is not possible to load the required pip modules and add them dynamically to the script excecution. So you need to re-run the script again with the available dependencies.

- TYPO3 error message: `Unknown column '?' in 'field list'` 
   
   Sometimes your local environment differ from the remote system. So you maybe need to update the database schema either manually via the install tool or using the TYPO3 console by `typo3cms database:updateschema`