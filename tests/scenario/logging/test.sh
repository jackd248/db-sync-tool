#!/bin/sh

#
# Option Logging
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing option logging"
echo "\033[94m[INFO]\033[m \033[90mSync: WWW1 -> WWW2, Initiator: WWW2\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool/sync.py -f /var/www/html/tests/scenario/logging/sync-www1-to-local.json -m
FILE=./files/test.log
if [ -f "$FILE" ]; then
    echo "\033[92m[SUCCESS]\033[m Log file created"
else
    echo "\033[91m[FAILURE]\033[m Log file not created"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"
