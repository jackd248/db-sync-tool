#!/bin/sh
#
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#
# Starting docker container
#
echo "\033[90m#####################################\033[m"
echo "\033[94m[INFO]\033[m Cleaning up files"
rm -rf ../files/www1/database_backup
rm -rf ../files/www2/database_backup

echo "\033[94m[INFO]\033[m Cleaning up databases"
cd ../docker
docker-compose exec db1 mysql -udb -pdb db -e 'DROP TABLE IF EXISTS person'
docker-compose exec db2 mysql -udb -pdb db -e 'DROP TABLE IF EXISTS person'
echo "\033[94m[INFO]\033[m Importing dump"
cat dump/db.sql | docker-compose exec -T db1 mysql -udb -pdb db
echo "\033[94m[INFO]\033[m Scenario reset"
echo "\033[90m#####################################\033[m"
