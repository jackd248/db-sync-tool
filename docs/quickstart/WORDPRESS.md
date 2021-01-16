# Quickstart Wordpress

The db-sync-tool can automatic detect the database credentials of a Wordpress application.

- [Wordpress](https://wordpress.org) (>= v5.0)

Therefore, you have to define the file path to the `wp-config.php`, which contains the needed credentials. See the [Wordpress documentation](https://wordpress.org/support/article/editing-wp-config-php/) for more information.

## Command line
Example call for a Drupal sync in [receiver mode](../MODE.md):

```bash
$ python3 db_sync_tool 
    --type WORDPRESS
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
  "type": "WORDPRESS",
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

It is possible to extend the [configuration](docs/CONFIG.md).