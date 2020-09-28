# Test environment

```bash
 $ sh helper/test.sh
```

```bash
 $ docker-compose up -d
```

```bash
 $ docker-compose exec www2 bash
```

```bash
 $ python3 /var/www/html/sync.py -f /var/www/html/test/scenario/sync-www1-to-local.json
```