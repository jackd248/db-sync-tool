# Quickstart Drupal

The db-sync-tool can automatic detect the database credentials of a Drupal application.

- [Drupal](https://www.drupal.org/) (>= v8.0)

Therefore, you have to define the path to the desired drupal installation. The script uses `drush` to extract the database settings. See the [Drush documentation](https://www.drush.org/latest/commands/core_status/) for more information.

## Command line
Example call for a Drupal sync in [receiver mode](../MODE.md):

```bash
$ python3 db_sync_tool 
    --type DRUPAL
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
  "type": "DRUPAL",
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