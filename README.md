# TYPO3 Database Sync

Simple python script to synchronize a TYPO3 database from a remote to your local system.

## Prerequisite

The script using python 2. It is necessary for some additional functionalities to have [pip](https://pypi.org/project/pip/) installed on your local machine. 
You can do this by the following command:

```bash
apt install -y python-pip
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
    "path": "../htdocs/typo3/web/typo3conf/LocalConfiguration.php"
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
-h, --help          Show help
-c, --config        Path to host file
```

You are requested to enter the SSH password for the given user in the `host.json` to enable a SSH connection to the remote system. 

### Ignore tables

Often it is better to exclude some tables from the sql dump for performance reasons, e.g. caching tables. There is a default stack of ignored tables within the script, but you can specify them in your `host.yml`. The following tables are the default setting:

```json
{
  ...
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
    'cf_extbase_reflection_tags'
  ]
}
```

## FAQ

- `Unknown column '?' in 'field list'` 
   
   Sometimes your local environment differ from the remote system. So you maybe need to update the database schema either manually via the install tool or using the TYPO3 console by `typo3cms database:updateschema`