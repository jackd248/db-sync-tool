#!/bin/sh

#
# Sync mode: IMPORT_LOCAL
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: IMPORT_LOCAL"
echo "\033[90m#############################################\033[m"
echo ""
tar -xvzf ./../files/www2/database_backup/test.sql.tar.gz -C ./../files/www2/database_backup/
docker-compose exec www2 python3 /var/www/html/sync.py -f /var/www/html/test/scenario/import_local/import-local.json -v 1 -i /var/www/html/test/files/www2/database_backup/test.sql