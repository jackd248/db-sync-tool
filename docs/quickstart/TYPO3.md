# Quickstart TYPO3

The db-sync-tool can automatic detect the database credentials of a TYPO3 application.

- [TYPO3](https://typo3.org/) (>= v7.6)

Therefore, you have to define the file path to the `LocalConfiguration.php`, which contains the needed credentials. See the [TYPO3 documentation](https://docs.typo3.org/m/typo3/reference-coreapi/10.4/en-us/ApiOverview/GlobalValues/Typo3ConfVars/Index.html) for more information.

## Command line
Example call for a TYPO3 sync in [receiver mode](../MODE.md):

```bash
$ python3 db_sync_tool 
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
$ python3 db_sync_tool 
    --config-file <PATH TO CONFIG FILE>
```

Example configuration file:
```json
{
  "type": "TYPO3",
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