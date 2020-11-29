#!/bin/sh

#
# Sync mode: IMPORT_REMOTE
#

printf "\033[94m[TEST]\033[m Sync mode: IMPORT_REMOTE"
printf " \033[90m(Sync: test.sql -> WWW1, Initiator: WWW2)\033[m"

mkdir -p ./files/www1/database_backup/
cp ./docker/dump/test.sql.tar.gz ./files/www1/database_backup/
tar -xvzf ./files/www1/database_backup/test.sql.tar.gz -C ./files/www1/database_backup/
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/import_remote/import-www1-from-local.json -i /var/www/html/tests/files/www1/database_backup/test.sql $1
# Expecting 3 results in the database
count=$(docker-compose exec db1 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi

sh helper/cleanup.sh

