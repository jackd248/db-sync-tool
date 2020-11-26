#!/bin/sh

#
# Sync mode: SENDER
#

echo "\033[94m[INFO]\033[m Testing sync mode: SENDER"
echo "\033[94m[INFO]\033[m \033[90mSync: WWW2 -> WWW1, Initiator: WWW2\033[m"
docker-compose exec www2 python3 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/sender/sync-local-to-www1.json -m

# Expecting 3 results in the database
count=$(docker-compose exec db1 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [[ $count == '|3|' ]]; then
    echo "\033[92m[SUCCESS]\033[m Synchronisation succeeded"
else
    echo "\033[91m[FAILURE]\033[m Synchronisation was not successful"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
sh helper/cleanup.sh
echo "\033[90m#############################################\033[m"
