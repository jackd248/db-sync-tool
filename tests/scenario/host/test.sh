#!/bin/sh

#
# Option Link
#

printf "\033[94m[TEST]\033[m Feature: Link"
printf " \033[90m(Sync: WWW1 -> PROXY -> WWW2, Initiator: PROXY)\033[m"
docker-compose exec proxy $1 /var/www/html/db_sync_tool -y -o /var/www/html/tests/scenario/link/hosts.json www1 www2 -t TYPO3 $2
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh