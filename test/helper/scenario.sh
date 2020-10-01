#!/bin/sh

#
# Starting shell script in helper directory
#
parent_path=$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)
cd "$parent_path"

#
# Starting docker container
#
echo "\033[90m#############################################\033[m"
echo "\033[94m[INFO]\033[m Starting docker container"
echo "\033[90m#############################################\033[m"
cd ./../docker
docker-compose up -d

if [ "$#" -eq "0" ]; then
  sh ../scenario/receiver/test.sh
  sh ../scenario/sender/test.sh
  sh ../scenario/proxy/test.sh
  sh ../scenario/dump_local/test.sh
  sh ../scenario/dump_remote/test.sh
  sh ../scenario/import_local/test.sh
  sh ../scenario/import_remote/test.sh
  sh ../scenario/symfony/test.sh
  sh ../scenario/logging/test.sh
  sh ../scenario/link/test.sh
  sh ../scenario/download/test.sh
else
  sh ../scenario/$1/test.sh
fi
