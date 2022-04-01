#!/bin/sh

#
# Feature: Post SQL
#

printf "\033[94m[TEST]\033[m Feature: Post SQL"
printf " \033[90m(Sync: WWW1 -> WWW2, Initiator: WWW2)\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/post_sql/sync-www1-to-local.yml -y $1

# Expecting 2 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 2 | tr -d '[:space:]')
if [[ $count == '|2|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh