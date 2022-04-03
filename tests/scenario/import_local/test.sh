#!/bin/sh

#
# Sync mode: IMPORT_LOCAL
#

printf "\033[94m[TEST]\033[m Sync mode: IMPORT_LOCAL"
printf " \033[90m(Sync: test.sql -> WWW2, Initiator: WWW2)\033[m"
mkdir -p ./files/www2/database_backup/
cp ./docker/dump/test.sql ./files/www2/database_backup/
docker-compose exec www2 $1 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/import_local/import-local.json -y -i /var/www/html/tests/files/www2/database_backup/test.sql $2
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi

sh helper/cleanup.sh