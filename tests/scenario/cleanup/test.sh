#!/bin/sh

#
# CleanUp
#

printf "\033[94m[TEST]\033[m Feature: CleanUp "
printf "\033[90m(Sync: WWW1 -> WWW1, Initiator: WWW2)\033[m"

#
# Testing file clean up
#
mkdir ./files/www1/database_backup
touch ./files/www1/database_backup/1.sql
touch ./files/www1/database_backup/2.sql
touch ./files/www1/database_backup/3.sql
touch ./files/www1/database_backup/4.sql
touch ./files/www1/database_backup/5.sql

docker-compose exec www2 $1 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/cleanup/dump-www1-from-local.json -y -dn test $2
FILE=./files/www1/database_backup/1.sql
if [ ! -f "$FILE" ]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh