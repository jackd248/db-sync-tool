#!/bin/sh

#
# Sync mode: DUMP_REMOTE
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: DUMP_REMOTE"

#
# Testing file clean up
#
mkdir ./../files/www1/database_backup
touch ./../files/www1/database_backup/1.sql
touch ./../files/www1/database_backup/2.sql
touch ./../files/www1/database_backup/3.sql
touch ./../files/www1/database_backup/4.sql
touch ./../files/www1/database_backup/5.sql

docker-compose exec www2 python3 /var/www/html/sync.py -f /var/www/html/test/scenario/dump_remote/dump-www1-from-local.json -m -dn test

FILE=./../files/www1/database_backup/test.sql.tar.gz
if [ -f "$FILE" ]; then
    echo "\033[92m[SUCCESS]\033[m Remote database dump file created"
    echo ""
else
    echo "\033[91m[FAILURE]\033[m Remote database dump file not created"
    echo "\033[90m#############################################\033[m"
    exit 1
fi

sh ../helper/cleanup.sh
echo "\033[90m#############################################\033[m"