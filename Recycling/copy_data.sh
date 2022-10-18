#!/bin/bash
if [ $# -ne 1 ]
then
  sudo echo "Enter honeypot name"
fi

curr_date=$(date +'%Y-%m-%d-%H%M')

sudo cp ./data/$1_log ./data/copied_logs/${curr_date}_$1_log

sudo echo "" > ./data/$1_log
