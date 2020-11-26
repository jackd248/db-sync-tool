#!/bin/sh

#
# CleanUp
#

echo "\033[94m[INFO]\033[m Testing clean up"
echo "\033[94m[INFO]\033[m \033[90mSync: WWW1 -> WWW1, Initiator: WWW2\033[m"

#
# Testing file clean up
#
mkdir ./files/www1/database_backup
touch ./files/www1/database_backup/1.sql
touch ./files/www1/database_backup/2.sql
touch ./files/www1/database_backup/3.sql
touch ./files/www1/database_backup/4.sql
touch ./files/www1/database_backup/5.sql

docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/cleanup/dump-www1-from-local.json -m -dn test
FILE=./files/www1/database_backup/1.sql
if [ ! -f "$FILE" ]; then
    echo "\033[92m[SUCCESS]\033[m Remote clean up successful"
else
    echo "\033[91m[FAILURE]\033[m Remote clean up not successful"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"