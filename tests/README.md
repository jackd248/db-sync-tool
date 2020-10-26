# Test environment

## Execution

Start the docker container:

```bash
 $ docker-compose up -d
```

All possible scenarios will be executed by the following command:

```bash
 $ sh helper/scenario.sh
```

You can also run one specific test case by using the command:

```bash
 $ sh helper/scenario.sh [scenario]
```

and select one of the following scenarios:

- download
- dump_local
- dump_remote
- import_local
- import_remote
- link
- logging
- proxy
- receiver
- sender
- symfony
- drupal