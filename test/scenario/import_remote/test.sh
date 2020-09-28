#!/bin/sh

#
# Sync mode: IMPORT_REMOTE
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: IMPORT_REMOTE"
echo "\033[90m#############################################\033[m"
echo ""
tar -xvzf ./../files/www1/database_backup/test.sql.tar.gz -C ./../files/www1/database_backup/
docker-compose exec www2 python3 /var/www/html/sync.py -f /var/www/html/test/scenario/import_remote/import-www1-from-local.json -v 1 -i /var/www/html/test/files/www1/database_backup/test.sql
#
# Reset scenario
#
sh ../helper/cleanup.sh

