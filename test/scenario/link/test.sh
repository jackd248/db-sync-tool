#!/bin/sh

#
#
#
echo ""
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Testing option link"
echo "\033[90m#############################################\033[m"
echo ""
docker-compose exec proxy python3 /var/www/html/sync.py -f /var/www/html/test/scenario/link/sync-www1-to-www2.json -o /var/www/html/test/scenario/link/hosts.json -v 1
#
# Reset scenario
#
sh ../helper/cleanup.sh
