#!/bin/sh

#
# Starting shell script in helper directory
#
parent_path=$(
  cd "$(dirname "${BASH_SOURCE[0]}")"
  pwd -P
)
cd "$parent_path"
cd ..

if [ "$#" -eq "0" ]; then
  sh scenario/receiver/test.sh
  sh scenario/sender/test.sh
  sh scenario/proxy/test.sh
  sh scenario/dump_local/test.sh
  sh scenario/dump_remote/test.sh
  sh scenario/import_local/test.sh
  sh scenario/import_remote/test.sh
  sh scenario/symfony/test.sh
  sh scenario/drupal/test.sh
  sh scenario/logging/test.sh
  sh scenario/link/test.sh
  sh scenario/download/test.sh
  sh scenario/cleanup/test.sh
else
  sh scenario/$1/test.sh
fi
