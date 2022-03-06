# Quickstart Symfony

The db-sync-tool can automatic detect the database credentials of a Symfony application.

- [Symfony](https://symfony.com/) (>= v2.8)

Therefore, you have to define the file path to the database configuration file.

For Symfony >= __3.4__ use the `.env` file containing the `DATABASE_URL` environment variable. See the [Doctrine documentation](https://symfony.com/doc/current/doctrine.html) for more information.

For Symfony <= __2.8__ use the `parameters.yml` file containing the database parameters. See the [Doctrine documentation](https://symfony.com/doc/3.4/doctrine.html) for more information.

## Command line
Example call for a Symfony sync in [receiver mode](../MODE.md):

```bash
$ python3 db_sync_tool 
    --type SYMFONY
    --origin-host <ORIGIN_HOST> 
    --origin-user <ORIGIN_USER>
    --origin-path <ORIGIN_PATH>
    --target-path <TARGET_PATH>
```

## Configuration file
For reusability reasons you can use an additional configuration file containing all necessary information about the sync.

Command line call:
```bash
$ python3 db_sync_tool 
    --config-file <PATH TO CONFIG FILE>
```

Example configuration file:
```json
{
  "type": "SYMFONY",
  "target": {
    "path": "<TARGET_PATH>"
  },
  "origin": {
    "host": "<ORIGIN_HOST>",
    "user": "<ORIGIN_USER>",
    "path": "<ORIGIN_PATH>"
  }
}
```

It is possible to extend the [configuration](../CONFIG.md).