#!/bin/bash

curr_date=$(date +'%m-%d-%Y')
sudo mkdir ./data/$curr_date

sudo cp ./data/DATABASE_1_log ./data/$curr_date
sudo cp ./data/DATABASE_2_log ./data/$curr_date
sudo cp ./data/DATABASE_3_log ./data/$curr_date
sudo cp ./data/DATABASE_4_log ./data/$curr_date

sudo echo "" > ./data/DATABASE_1_log
sudo echo "" > ./data/DATABASE_2_log
sudo echo "" > ./data/DATABASE_3_log
sudo echo "" > ./data/DATABASE_4_log