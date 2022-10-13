#!/bin/bash

curr_date=$(date +'%m-%d-%Y')
mkdir ~/data/$curr_date

cp ~/data/DATABASE_1_log ~/data/$curr_date
cp ~/data/DATABASE_2_log ~/data/$curr_date
cp ~/data/DATABASE_3_log ~/data/$curr_date
cp ~/data/DATABASE_4_log ~/data/$curr_date

echo "" > ~/data/DATABASE_1_log
echo "" > ~/data/DATABASE_2_log
echo "" > ~/data/DATABASE_3_log
echo "" > ~/data/DATABASE_4_log
