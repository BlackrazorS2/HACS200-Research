#!/bin/bash
honeypot_ip=$(sudo cat ./properties/$1_properties | cut -d' ' -f1)
sudo ./recycler.sh $1 $honeypot_ip 1