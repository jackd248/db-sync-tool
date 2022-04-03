#!/bin/sh

#
# Option Logging
#

printf "\033[94m[TEST]\033[m Feature: Logging"
printf " \033[90m(Sync: WWW1 -> WWW2, Initiator: WWW2)\033[m"
docker-compose exec www2 $1 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/logging/sync-www1-to-local.json -y $2
FILE=./files/test.log
if [ -f "$FILE" ]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh
