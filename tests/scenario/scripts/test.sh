#!/bin/sh

#
# Feature: Scripts
#

printf "\033[94m[TEST]\033[m Feature: Scripts"
printf " \033[90m(Sync: WWW1 -> WWW2, Initiator: WWW2)\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/scripts/sync-www1-to-local.json -y $1

# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 4 | tr -d '[:space:]')
if [ $count == '|4|' ] && [ -f "./files/www1/before_script.txt" ] && [ -f "./files/www1/after_script.txt" ] && [ -f "./files/www2/before_script.txt" ] && [ -f "./files/www2/after_script.txt" ] && [ -f "./files/www1/before_script_global.txt" ] && [ -f "./files/www1/after_script_global.txt" ]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh