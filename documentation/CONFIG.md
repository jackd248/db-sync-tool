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

### Temporary dump directory

Normally is the script creating the sql dump in the `home` directory of the given ssh user. If this directory is not writable, you can specify an alternative directory in the `host.json`, where the temporary sql dump will be saved:

```json
{
  "origin": {
    "dump_dir": "/path/to/writable/dir/"
  }
}
```

### Check dump

The script is checking the target dump if the file is being downloaded completely. If you want to prevent this check, you can disable them in the `host.json`:

```json
{
  "check_dump": false
}
```