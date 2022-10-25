#!/bin/bash

# takes three arguments being the username, paswword and ip of the host
if [$# -ne 3]
then
    echo "Usage: dataTransfer.sh [username] [password] [ip]"
    exit 1
fi

path="/home/student/data/copied_data" # extra workstation vm


sudo rsync -avuh -e ssh "$path/*" $1@$3:/home/$1/HACS200-Research-Data-Backup/
expect "password:"
send $2
expect "*\r"   
expect "\r"  
