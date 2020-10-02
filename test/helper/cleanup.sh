#!/bin/sh
#
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#
# Starting docker container
#
# Cleaning up files
rm -rf ../files/www1/database_backup
rm -rf ../files/www2/database_backup
rm -rf ../files/test.log
rm -rf ../files/www2/download

# Remove database tables
cd ../docker
docker-compose exec db1 mysql -udb -pdb db -e 'DROP TABLE IF EXISTS person' > /dev/null
docker-compose exec db2 mysql -udb -pdb db -e 'DROP TABLE IF EXISTS person' > /dev/null
# Import database dump
cat dump/db.sql | docker-compose exec -T db1 mysql -udb -pdb db > /dev/null
echo "\033[94m[INFO]\033[m Scenario reset"
