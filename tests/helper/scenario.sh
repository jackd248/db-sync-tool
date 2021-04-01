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

VERBOSE="-m"

if [ "$#" -eq "0" ]; then
  sh scenario/receiver/test.sh $VERBOSE
  sh scenario/sender/test.sh $VERBOSE
  sh scenario/proxy/test.sh $VERBOSE
  sh scenario/dump_local/test.sh $VERBOSE
  sh scenario/dump_remote/test.sh $VERBOSE
  sh scenario/import_local/test.sh $VERBOSE
  sh scenario/import_remote/test.sh $VERBOSE
  sh scenario/sync_remote/test.sh $VERBOSE
  sh scenario/sync_remote_manual/test.sh $VERBOSE
  sh scenario/sync_local/test.sh $VERBOSE
  sh scenario/symfony/test.sh $VERBOSE
  sh scenario/laravel/test.sh $VERBOSE
  sh scenario/symfony2.8/test.sh $VERBOSE
  sh scenario/drupal/test.sh $VERBOSE
  sh scenario/wordpress/test.sh $VERBOSE
  sh scenario/typo3v7/test.sh $VERBOSE
  sh scenario/logging/test.sh $VERBOSE
  sh scenario/link/test.sh $VERBOSE
  sh scenario/download/test.sh $VERBOSE
  sh scenario/cleanup/test.sh $VERBOSE
  sh scenario/module/test.sh $VERBOSE
  sh scenario/manual/test.sh $VERBOSE
  sh scenario/shell/test.sh $VERBOSE
  sh scenario/scripts/test.sh $VERBOSE
  sh scenario/yaml/test.sh $VERBOSE
else
  # Default is mute mode
  if [ -z "$2" ]; then
    VERBOSE="-m"
  else
    VERBOSE=$2
  fi
  sh scenario/$1/test.sh $VERBOSE
fi
