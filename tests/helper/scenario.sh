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
PYTHON="python3"

if [ "$#" -eq "0" ]; then
  for d in "scenario/"*
  do
    sh $d/test.sh $PYTHON $VERBOSE
  done
else
  # Default is mute mode
  if [ -z "$2" ]; then
    VERBOSE="-m"
  else
    VERBOSE=$2
  fi
  sh scenario/$1/test.sh $PYTHON $VERBOSE
fi
