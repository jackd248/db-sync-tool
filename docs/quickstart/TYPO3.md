# Quickstart TYPO3

The db-sync-tool can automatically detect the database credentials of a TYPO3 application.

- [TYPO3](https://typo3.org/) (>= v7.6)

Therefore, you have to define the file path to the `LocalConfiguration.php`, which contains the needed credentials. See the [TYPO3 documentation](https://docs.typo3.org/m/typo3/reference-coreapi/10.4/en-us/ApiOverview/GlobalValues/Typo3ConfVars/Index.html) for more information.

## Command line
Example call for a TYPO3 sync in [receiver mode](../MODE.md):

```bash
$ db_sync_tool 
    --type TYPO3
    --origin-host <ORIGIN_HOST> 
    --origin-user <ORIGIN_USER>
    --origin-path <ORIGIN_PATH>
    --target-path <TARGET_PATH>
```

## Configuration file
For reusability reasons you can use an additional configuration file containing all necessary information about the sync.

Command line call:
```bash
$ db_sync_tool 
    --config-file <PATH TO CONFIG FILE>
```

The configuration file should look like:

```yaml
type: TYPO3
target:
    path: <TARGET_PATH>
origin:
    host: <ORIGIN_HOST>
    user: <ORIGIN_USER>
    path: <ORIGIN_PATH>
```

It is possible to extend the [configuration](../CONFIG.md).

## Example

Here is an extended example with demo data:

```yaml
type: TYPO3
target:
    path: /var/www/html/htdocs/typo3/web/typo3conf/LocalConfiguration.php
origin:
    host: 192.87.33.123
    user: ssh_demo_user
    path: /var/www/html/shared/typo3conf/LocalConfiguration.php
    name: Demo Prod
ignore_table:
    - be_users
    - sys_domain 
    - cf_cache_*
```

## .env support

Alternatively, the credentials can be parsed out of an `.env` file. If the `path` configuration points to a `.env` file, the db-sync-tool will try to parse the database credentials from it. The `.env` file should contain the following variables:

```dotenv
# .env Database Default Configuration Keys
TYPO3_CONF_VARS__DB__Connections__Default__host=db
TYPO3_CONF_VARS__DB__Connections__Default__port=3306
TYPO3_CONF_VARS__DB__Connections__Default__password=db
TYPO3_CONF_VARS__DB__Connections__Default__user=db
TYPO3_CONF_VARS__DB__Connections__Default__dbname=db
```

If the `.env` file contains different keys for the database credentials, you can specify them in the configuration file:

```yaml
type: TYPO3
target:
    path: /var/www/html/.env
origin:
    name: Demo Prod
    host: 123.456.78.90
    user: ssh_demo_user
    path: /var/www/html/shared/.env
    db:
        name: TYPO3_DB_NAME
        host: TYPO3_DB_HOST
        user: TYPO3_DB_USER
        password: TYPO3_DB_PASSWORD
ignore_table:
    - cf_cache_*
```
