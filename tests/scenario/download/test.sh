#!/bin/sh

#
# Download dump
#

printf "\033[94m[TEST]\033[m Feature: Download Dump File "
printf "\033[90m(Sync: WWW1 -> WWW2 (dump.sql), Initiator: WWW2)\033[m"
docker-compose exec www2 $1 /var/www/html/db_sync_tool -f /var/www/html/tests/scenario/download/sync-www1-to-local.json -kd /var/www/html/tests/files/www2/download/ -y -dn dump $2

FILE=./files/www2/download/dump.sql
if [ -f "$FILE" ]; then
    echo " \033[92m✔\033[m"
else
    echo " \033[91m✘\033[m"
    exit 1
fi
sh helper/cleanup.sh