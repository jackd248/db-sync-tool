# Quickstart

If you don't want to use the automatic database credential detection of a supported framework, you can define all needed credentials by your own. 

## Command line
Almost all sync features can be declared via the command line call. This is an example for a sync in [receiver mode](../MODE.md):

```bash
$ python3 db_sync_tool 
    --origin-host <ORIGIN_HOST> 
    --origin-user <ORIGIN_USER>
    --origin-db-name <ORIGIN_DB_NAME>
    --origin-db-user <ORIGIN_DB_USER>
    --origin-db-password <ORIGIN_DB_PASSWORD>
    --target-db-name <TARGET_DB_NAME>
    --target-db-user <TARGET_DB_USER>
    --target-db-password <TARGET_DB_PASSWORD>
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
  "target": {
    "db": {
      "name": "<TARGET_DB_NAME>",
      "password": "<TARGET_DB_PASSWORD>",
      "user": "<TARGET_DB_USER>"
    }
  },
  "origin": {
    "host": "<ORIGIN_HOST>",
    "user": "<ORIGIN_USER>",
    "db": {
      "name": "<ORIGIN_DB_NAME>",
      "password": "<ORIGIN_DB_PASSWORD>",
      "user": "<ORIGIN_DB_USER>"
    }
  }
}
```

It is possible to extend the [configuration](docs/CONFIG.md).