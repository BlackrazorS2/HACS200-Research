#!/bin/bash

# takes three arguments being the username, paswword and ip of the host
if [ $# -ne 3 ]
then
    echo "Usage: dataTransfer.sh [username] [password] [ip]"
    exit 1
fi

path="/home/student/data/copied_data" # extra workstation vm

sudo sshpass -p $2 scp -r $1 "$path/*" $1@$3:/home/$1/HACS200-Research-Data-Backup/