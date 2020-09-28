#!/bin/sh

#
# Option Link
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing option link"
docker-compose exec proxy python3 /var/www/html/sync.py -f /var/www/html/test/scenario/link/sync-www1-to-www2.json -o /var/www/html/test/scenario/link/hosts.json -m
# Expecting 3 results in the database
count=$(docker-compose exec db2 mysql -udb -pdb db -e 'SELECT COUNT(*) FROM person' | grep 3 | tr -d '[:space:]')
if [ $count == '|3|' ]; then
    echo "\033[92m[SUCCESS]\033[m Synchronisation succeeded"
    echo "\033[90m#############################################\033[m"
else
    echo "\033[91m[FAILURE]\033[m Synchronisation was not successful"
    echo "\033[90m#############################################\033[m"
    exit 1
fi
#
# Reset scenario
#
sh ../helper/cleanup.sh
