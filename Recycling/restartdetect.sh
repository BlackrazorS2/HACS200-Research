#!/bin/bash

# kills all detectexit listeners for each honeypot and restarts them

sudo killall inotifywait

sudo echo "Killed all exit listeners"

if [ -f data/DATABASE_1_log ]
then
        sudo echo "detectexit 1"
        sudo ./detectexit.sh 1 &
fi

if [ -f data/DATABASE_2_log ]
then
        sudo echo "detectexit 2"
        sudo ./detectexit.sh 2 &
fi

if [ -f data/DATABASE_3_log ]
then
        sudo echo "detectexit 3"
        sudo ./detectexit.sh 3 &
fi

if [ -f data/DATABASE_4_log ]
then
        sudo echo "detectexit 4"
        sudo ./detectexit.sh 4 &
fi

sudo echo "Rebooted all exit listeners"
