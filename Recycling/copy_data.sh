#!/bin/bash
if [ $# -ne 1 ]
then
  sudo echo "Enter honeypot name"
fi

curr_date=$(date +'%Y-%m-%d-%H%M')
sudo mkdir ./data/$curr_date

sudo cp ./data/$1_log ./data/$curr_date

sudo echo "" > ./data/$1_log
