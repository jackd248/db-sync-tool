# Configuration

Here you can find an overview over the possible configuration adjustments.

- [Full configuration reference](#configuration_reference)
- [Ignore tables](#ignore_tables)
- [Authentication](#authentication)
- [Linking hosts](#linking)
- [SSH Port](#port)
- [Console commands](#console)
- [(Temporary) dump directory](#directory)
- [Before and after script](#script)
- [After dump](#after-dump)
- [Logging](#logging)
- [Cleaning up / keeping dumps count](#clean_up)
- [Naming hosts](#naming)
- [Check dump](#check)
- [Manual database credentials](#manual)

<a name="configuration_reference"></a>
### Full configuration reference

```json
{
  "name": "project",
  "type": "type",
  "target": {
    "name": "name",
    "link": "@link",
    "host": "www1",
    "user": "user",
    "port": 22,
    "password": "password",
    "ssh_key": "ssh_key",
    "dump_dir": "/path/to/writable/dir/",
    "db": {
      "name": "db",
      "host": "db2",
      "password": "db",
      "user": "db",
      "port": 3306
    },
    "after_script": "",
    "script": {
      "before": "",
      "after": "",
      "error": ""
    },
    "console": {
      "php": "/usr/bin/php"
    },
    "keep_dumps": 5,
    "after_dump": "path/to/dump/file.sql"
  },
  "origin": {
    "name": "name",
    "link": "@link",
    "host": "www1",
    "user": "user",
    "port": 22,
    "password": "password",
    "ssh_key": "ssh_key",
    "dump_dir": "/path/to/writable/dir/",
    "db": {
      "name": "db",
      "host": "db1",
      "password": "db",
      "user": "db",
      "port": 3306
    },
    "script": {
      "before": "",
      "after": "",
      "error": ""
    },
    "console": {
      "php": "/usr/bin/php"
    }
  },
  "log_file": "/path/to/file/info.log",
  "ignore_table": [],
  "check_dump": false
}
```

<a name="ignore_tables"></a>
### Ignore tables 

Often it is better to exclude some tables from the sql dump for performance reasons, e.g. caching tables. Specify them as comma separated list in the `ignore_table` array.

You can use wildcards to define several tables:

```json
{
  "ignore_table": [ 
    "cache_*"
  ]  
}
```

<a name="authentication"></a>
### Authentication

If you want to authenticate with a private ssh key instead of a user entered password to the server (useful for CI/CD), you can add the file path to the private key file in your `config.json`:

```json
{
  "origin": {
    "ssh_key": "~/bob/.ssh/id_rsa"
  }
}
```

It's not recommended, but you can also specify the plain password inside the host configuration in the `config.json`:

```json
{
  "origin": {
    "password": "1234"
  }
}
```

<a name="linking"></a>
### Linking hosts

For larger project setups with multiple configuration files, it's better to reuse the host configuration in every sync scenario. So you can link to predefined host in your `config.json`:

```json
{
  "origin": {
    "link": "@prod"
  },
  "target": {
    "link": "@dev"
  }
}
```

You specify the path to the `hosts.json` file with the `-o` option within the script call. The `hosts.json` should look like this:

```json
{
  "prod": {
    "host": "host",
    "user": "user",
    "path": "/var/www/html/project/shared/typo3conf/LocalConfiguration.php"
  },
  "dev": {
    "host": "host",
    "user": "user",
    "path": "/var/www/html/project/shared/typo3conf/LocalConfiguration.php"
  }
}
```


<a name="port"></a>
### SSH Port

You can also specify a different SSH port to the client in your `config.json` (the default port is `22`):

```json
{
  "origin": {
    "port": "1234"
  }
}
```

<a name="console"></a>
### Console commands

The script using among other things the `php`, `mysql`, `mysqldump`, `grep` commands to synchronize the databases. Sometimes these commands are not available via the path variable, so you have to specify the full path to the source in the `config.json` depending on the system:

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

<a name="directory"></a>
### (Temporary) dump directory

Normally is the script creating the sql dump in the `/tmp/` directory. If this directory is not writable or you want to export the database automatically in another directory, you can specify an alternative directory in the `config.json`, where the temporary sql dump will be saved:

```json
{
  "origin": {
    "dump_dir": "/path/to/writable/dir/"
  }
}
```

**Note:** It is recommended to use for every application another directory to avoid side effects (e.g. cleaning up feature).

<a name="script"></a>
### Before and after script

Sometimes it is necessary to run a specific command before or after the dump creation on the origin or target system to ensure the correct synchronisation process. Therefore you can specify these commands in the `config.json`:

```json
{
  "script": {
    "before": "",
    "after": "",
    "error": ""
  },
  "origin": {
    "script": {
      "before": "",
      "after": "",
      "error": ""
    },
  },
  "target": {
    "script": {
      "before": "",
      "after": "",
      "error": ""
    },
  }
}
```

<a name="after-dump"></a>
### After dump

It is possible to provide an additional dump file, which will be imported after the regular database import is finished. You can specify the path to the `after_dump` file of the target host in the `config.json`:

```json
{
  "target": {
    "after_dump": "path/to/dump/file.sql"
  }
}
```

<a name="logging"></a>
### Logging

You can enable the logging to a separate log file via the `log_file` entry in the `config.json`:

```json
{
  "log_file": "/path/to/file/info.log"
}
```

**Note**: By default only a summary of the sync actions will be logged. If you enable the verbose option (`-v`) all console output will also be logged in the given log file.

<a name="clean_up"></a>
### Cleaning up / keeping dumps count

With the concept of the *DUMP_REMOTE* or *DUMP_LOCAL* mode can you implement an automatic backup system. However it's a good option to clean up old dump files and only keep the newest ones. Therefore you can use the `keep_dumps` entry in the `config.json`:

```json
{
  "origin": {
    "dump_dir": "/path/to/writable/dir/",
    "keep_dumps": 5
  }
}
```

**Note**: Be aware of this feature. It will only keep the latest (e.g. 5) files in the `dump_dir` directory and delete all other `.sql` and `.tar.gz` files.

<a name="naming"></a>
### Naming hosts

For a better differentiation of the different host systems you can optionally provide a specific name in the `config.json`:

```json
{
  "origin": {
    "name": "Prod"
  },
  "target": {
    "name": "Stage"
  }
}
```

<a name="check"></a>
### Check dump

The script is checking the target dump if the file is being downloaded completely. If you want to prevent this check, you can disable them in the `config.json`:

```json
{
  "check_dump": false
}
```

<a name="manual"></a>
### Manual database credentials

It is also possible to skip the automatic database credential detection depending on the framework and provide the database credentials by your own in the `config.json` (example for RECEIVER mode):

```json
{
  "name": "project",
  "target": {
    "db": {
      "name": "db",
      "host": "db2",
      "password": "db",
      "user": "db",
      "port": 3306
    }
  },
  "origin": {
    "host": "www1",
    "user": "user",
    "password": "password",
    "db": {
      "name": "db",
      "host": "db1",
      "password": "db",
      "user": "db",
      "port": 3306
    }
  },
  "ignore_table": []
}
```