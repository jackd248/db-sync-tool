#!/bin/sh

#
# Framework TYPO3 AdditionalConfiguration
#

printf "\033[94m[TEST]\033[m Application: TYPO3 AdditionalConfiguration"
printf " \033[90m(Sync: WWW1 -> WWW2, Initiator: WWW2)\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/typo3_additional/sync-www1-to-local.json -y $1
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh
