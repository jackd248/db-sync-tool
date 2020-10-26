#!/bin/sh

#
# Download dump
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing dump download"
echo "\033[94m[INFO]\033[m \033[90mSync: WWW1 -> WWW2 (dump.sql), Initiator: WWW2\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool/sync.py -f /var/www/html/tests/scenario/download/sync-www1-to-local.json -m -kd /var/www/html/tests/files/www2/download/ -dn dump

FILE=./files/www2/download/dump.sql
if [ -f "$FILE" ]; then
    echo "\033[92m[SUCCESS]\033[m Local database dump file created"
else
    echo "\033[91m[FAILURE]\033[m Local database dump file not created"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"