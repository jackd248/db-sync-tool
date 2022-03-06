#!/bin/sh

#
# Option Link Inline
#

printf "\033[94m[TEST]\033[m Feature: Link Inline"
printf " \033[90m(Sync: WWW1 -> PROXY -> WWW2, Initiator: PROXY)\033[m"
docker-compose exec proxy python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/link_inline/sync-www1-to-www2.yaml -y $1
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh