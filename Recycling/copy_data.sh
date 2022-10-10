#!/bin/bash

curr_date=$(date +'%m-%d-%Y')
mkdir ~/data/$curr_date

cp ~/data/honeypot1_log ~/data/$curr_date
cp ~/data/honeypot2_log ~/data/$curr_date
cp ~/data/honeypot3_log ~/data/$curr_date
cp ~/data/honeypot4_log ~/data/$curr_date

rm -f ~/data/honeypot1_log
rm -f ~/data/honeypot2_log
rm -f ~/data/honeypot3_log
rm -f ~/data/honeypot4_log
