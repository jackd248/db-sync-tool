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
- dump_local
- dump_remote
- import_local
- import_remote
- sync_remote
- sync_remote_manual
- sync_local
- link
- logging
- manual
- module
- proxy
- receiver
- scripts
- yaml
- host
- shell
- sender
- symfony
- symfony2.8
- drupal
- typo3v7
- wordpress
- laravel