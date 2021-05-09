#!/bin/bash

perform_mode="generate"
all_flag="false"
days_before=1

func() {
    echo "Usage:"
    echo "run.sh [-g] [-a] [-d days]"
}

while getopts "gad:" OPT; do
    case $OPT in
        g) perform_mode="generate";;
        a) all_flag="true";;
        d) days_before=$OPTARG;;
        ?) func;;
    esac
done

if [ $perform_mode = "generate" ]; then
  if [ $all_flag = "true" ]; then
      if [ "$days_before" != 1 ]; then
          python run.py --days="$days_before" --all
      fi
  else
    if [ "$days_before" -ge 0 ]; then
        python run.py --days="$days_before"
    fi
  fi
else
  echo "Invalid Option Selected"
fi

#if [ "$1" = "generate" ]; then
#  python run.py --days=1
#elif [ "$1" = "generate_all" ]; then
#  for (( i = 63; i > 0; i-- )); do
#        python run.py --days="$i"
#  done
#else
#	echo "Invalid Option Selected"
#fi