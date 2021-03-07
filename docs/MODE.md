# Sync modes

It is possible to enable different kind of sync modes for the database synchronisation depending on the preferred origin (which provides the database dump) and target system (which getting the database dump). 

The default mode is _receiver_. 

## Receiver

The _receiver_ mode offers the possibility to get a database dump from a remote system (origin) to your local system (target). 

![Sync mode receiver](images/sync-mode-receiver.png)

This mode is enabled, if a `host` entry is __only__ be stored in the `origin` section of the `config.json` configuration.

## Sender

The _sender_ mode offers the possibility to provide a database dump from your local system (origin) to a remote system (target). 

![Sync mode sender](images/sync-mode-sender.png)

This mode is enabled, if a `host` entry is __only__ be stored in the `target` section of the `config.json` configuration.

## Proxy

The _proxy_ mode offers the possibility to get a database dump from a remote system (origin) and store them temporarily on your local system. After that the stored database dump will be forwarded to another remote system (target).

![Sync mode proxy](images/sync-mode-proxy.png)

This mode can be used, when origin and target system can't or shouldn't connect directly (because of security restrictions). So your local system acts as proxy between both of them.  

This mode is enabled, if a `host` entry is be stored in the `origin` __and__ `target` section of the `config.json` configuration.

## Dump Local

The _dump local_ mode offers the possibility to only save a database dump from your local system. This is not really a synchronisation mode, just an easy way to save a database dump on your local maschine. No file transfer or database import will be performed. You can specify the dump file location with the `dump_dir` setting in your `config.json`.

![Sync mode sender](images/sync-mode-dump-local.png)

This mode is enabled, if _no_ `host` entry is be stored in the `target` or `origin` section of the `config.json` configuration.

## Dump Remote

The _dump local_ mode offers the possibility to only save a database dump from your local system. This is not really a synchronisation mode, just an easy way to save a database dump on a remote maschine (e.g. as backup mechanism). No file transfer or database import will be performed. You can specify the dump file location with the `dump_dir` setting in your `config.json`.

![Sync mode sender](images/sync-mode-dump-remote.png)

This mode is enabled, if the `host` entry are equal in the `target` and `origin` section of the `config.json` configuration.

## Import Local

The _import local_ mode offers the possibility to only import a database dump from a local file dump. This is not really a synchronisation mode, just an easy way to import a database dump on your local maschine. No file transfer will be performed.

![Sync mode sender](images/sync-mode-dump-local.png)

This mode is enabled, if you add the `-i` or `--import-file` option and specify the location of the local dump file.

## Import Remote

The _import remote_ mode offers the possibility to only import a database dump on a remote file dump. This is not really a synchronisation mode, just an easy way to import a database dump on a remote maschine. No file transfer will be performed.

![Sync mode sender](images/sync-mode-dump-remote.png)

This mode is enabled, if you add the `-i` or `--import-file` option, specify the location of the remote dump file and the `target` in your `config.json` is a remote system.

## Sync Local

The _sync local_ mode offers the possibility to sync a database within your local system (origin/target). 

![Sync mode receiver](images/sync-mode-sync-local.png)

This mode is enabled, if no `host` entry is stored and the `path` entries differ in the `config.json` configuration.

## Sync Remote

The _sync remote_ mode offers the possibility to sync a database within a remote system (origin/target). 

![Sync mode receiver](images/sync-mode-sync-remote.png)

This mode is enabled, if the `host` entries will be the same and the `path` entries differ in the `config.json` configuration.
