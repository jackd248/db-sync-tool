#!/bin/sh

# Sync mode: DUMP_LOCAL
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: DUMP_LOCAL"
echo "\033[94m[INFO]\033[m \033[90mSync: WWW2 -> test.sql, Initiator: WWW2\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool/sync.py -f /var/www/html/tests/scenario/dump_local/dump-local.json -m -dn test

FILE=./files/www2/database_backup/test.sql.tar.gz
if [ -f "$FILE" ]; then
    echo "\033[92m[SUCCESS]\033[m Local database dump file created"
else
    echo "\033[91m[FAILURE]\033[m Local database dump file not created"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"