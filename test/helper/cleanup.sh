#!/bin/sh
#
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
cd "$parent_path"
#
# Starting docker container
#
echo "\033[90m#####################################\033[m"
echo "\033[94m[INFO]\033[m Cleaning up files"
echo "\033[90m#####################################\033[m"
rm -rf ../files/www1/database_backup
rm -rf ../files/www2/database_backup

echo "\033[90m#####################################\033[m"
echo "\033[94m[INFO]\033[m Cleaning up databases"
echo "\033[90m#####################################\033[m"
cd ../docker
docker-compose exec db1 mysql -udb -pdb db -e 'DROP TABLE person'
docker-compose exec www2 mysql -udb -pdb -hdb2 db -e 'DROP TABLE person'
cat dump/db.sql | docker-compose exec -T db1 mysql -udb -pdb db
