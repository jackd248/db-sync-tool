#!/bin/sh

#
# Sync mode: DUMP_REMOTE
#

printf "\033[94m[TEST]\033[m Sync mode: DUMP_REMOTE"
printf " \033[90m(Sync: WWW1 -> test.sql, Initiator: WWW2)\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/dump_remote/dump-www1-from-local.json -y -dn test $1
FILE=./files/www1/database_backup/test.sql.tar.gz
if [ -f "$FILE" ]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh