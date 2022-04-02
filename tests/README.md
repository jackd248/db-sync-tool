# Test environment

## Execution

Start the docker container:

```bash
 $ docker-compose up -d
```

Install python dependencies in the containers:

```bash
 $ docker-compose exec www1 pip3 install -r requirements.txt
 $ docker-compose exec www2 pip3 install -r requirements.txt
 $ docker-compose exec proxy pip3 install -r requirements.txt
```

All possible scenarios will be executed by the following command:

```bash
 $ sh helper/scenario.sh
```

You can also run one specific test case by using the command:

```bash
 $ sh helper/scenario.sh [scenario]
```

Use the verbose argument to enable extended console output:

```bash
 $ sh helper/scenario.sh [scenario] -v
```

Select one of the following scenarios:

- cleanup
- download
- drupal
- dump_local
- dump_remote
- host
- import_local
- import_remote
- laravel
- link
- link_inline
- logging
- manual
- module
- overwrite
- post_sql
- proxy
- receiver
- reverse
- rsync
- scripts
- sender
- shell
- symfony
- symfony2.8
- sync_local
- sync_remote
- sync_remote_manual
- tables
- truncate
- typo3_additional
- typo3v7
- wordpress
- yaml