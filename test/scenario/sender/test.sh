#!/bin/sh

#
# Sync mode: SENDER
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing sync mode: SENDER"
echo "\033[90m#############################################\033[m"
echo ""
docker-compose exec www2 python3 /var/www/html/sync.py -f /var/www/html/test/scenario/sender/sync-local-to-www1.json -v 1
#
# Reset scenario
#
sh ../helper/cleanup.sh
