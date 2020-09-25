# Configuration

Here you can find an overview over the possible configuration adjustments.

### Ignore tables

Often it is better to exclude some tables from the sql dump for performance reasons, e.g. caching tables. Specify them as comma separeted list in the `ignore_table` array.

### SSH key authentification

If you want to authenticate with a private ssh key instead of a password to the server (useful for CI/CD), you can add the file path to the private key file in your `host.json`:

```json
{
  "origin": {
    "ssh_key": "~/bob/.ssh/id_rsa"
  }
}
```

### SSH Port

You can also specify a different SSH port to the client in your `host.json` (the default port is `22`):

```json
{
  "origin": {
    "port": "1234"
  }
}
```

### Console commands

The script using among other things the `php`, `mysql`, `mysqldump`, `grep` commands to synchronize the databases. Sometimes these commands are not available via the path variable, so you have to specify the full path to the source in the `host.json` depending on the system:

```json
{
  "origin": {
    "console": {
      "php": "/usr/bin/php",
      "mysql": "/usr/bin/mysql",
      "mysqldump": "/usr/bin/mysqldump"
    }
  }
}
```

### (Temporary) dump directory

Normally is the script creating the sql dump in the `home` directory of the given ssh user. If this directory is not writable or you want to export the database automatically in another directory, you can specify an alternative directory in the `host.json`, where the temporary sql dump will be saved:

```json
{
  "origin": {
    "dump_dir": "/path/to/writable/dir/"
  }
}
```

**Note:** It is recommended to use for every application another directory to avoid side effects (e.g. cleaning up feature).

### Before and after script

Sometimes it is necessary to run a specific command before or after the dump creation on the origin or target system to ensure the correct synchronisation process. Therefore you can specify these commands in the `host.json`:

```json
{
  "origin": {
    "before_script": "",
    "after_script": ""
  },
  "target": {
    "before_script": "",
    "after_script": ""
  }
}
```

### Logging

You can enable the logging to a separate log file via the `log_file` entry in the `host.json`:

```json
{
  "log_file": "/path/to/file/info.log"
}
```

**Note**: By default only a summary of the sync actions will be logged. If you enable the verbose option (`-v`) all console output will also be logged in the given log file.

### Cleaning up / keeping dumps count

With the concept of the *DUMP_REMOTE* or *DUMP_LOCAL* mode can you implement an automatic backup system. However it's a good option to clean up old dump files and only keep the newest ones. Therefore you can use the `keep_dumps` entry in the `host.json`:

```json
{
  "origin": {
    "dump_dir": "/path/to/writable/dir/",
    "keep_dumps": 5
  }
}
```

**Note**: Be aware of this feature. It will only keep the latest (e.g. 5) files in the `dump_dir` directory and delete all other `.sql` and `.tar.gz` files.

### Check dump

The script is checking the target dump if the file is being downloaded completely. If you want to prevent this check, you can disable them in the `host.json`:

```json
{
  "check_dump": false
}
```