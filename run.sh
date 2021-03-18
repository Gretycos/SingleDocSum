#!/bin/bash

if [ "$1" = "generate" ]; then
  python run.py --days=1
elif [ "$1" = "generate_all" ]; then
  for (( i = 89; i > 0; i-- )); do
        python run.py --days="$i"
  done
else
	echo "Invalid Option Selected"
fi


