#!/bin/sh

#
# Sync mode: IMPORT_LOCAL
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: IMPORT_LOCAL"
echo "\033[94m[INFO]\033[m \033[90mSync: test.sql -> WWW2, Initiator: WWW2\033[m"
mkdir -p ./../files/www2/database_backup/
cp ./../docker/dump/test.sql ./../files/www2/database_backup/
docker-compose exec www2 python3 /var/www/html/db_sync_tool/sync.py -f /var/www/html/tests/scenario/import_local/import-local.json -m -i /var/www/html/tests/files/www2/database_backup/test.sql
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo "\033[92m[SUCCESS]\033[m Import succeeded"
else
    echo "\033[91m[FAILURE]\033[m Import was not successful"
    echo "\033[90m#############################################\033[m"
    exit 1
fi

sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"