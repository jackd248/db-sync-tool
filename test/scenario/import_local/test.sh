#!/bin/sh

#
# Sync mode: IMPORT_LOCAL
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: IMPORT_LOCAL"

tar -xvzf ./../files/www2/database_backup/test.sql.tar.gz -C ./../files/www2/database_backup/
docker-compose exec www2 python3 /var/www/html/sync.py -f /var/www/html/test/scenario/import_local/import-local.json -m -i /var/www/html/test/files/www2/database_backup/test.sql
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [ $count == '|3|' ]; then
    echo "\033[92m[SUCCESS]\033[m Import succeeded"
    echo "\033[90m#############################################\033[m"
else
    echo "\033[91m[FAILURE]\033[m Import was not successful"
    echo "\033[90m#############################################\033[m"
    exit 1
fi