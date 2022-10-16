#!/bin/bash

# kills all detectexit listeners for each honeypot and restarts them

killall inotifywait

echo "Killed all exit listeners"

if [ -f data/DATABASE_1_log ]
then
        ./detectexit.sh 1 &
fi

if [ -f data/DATABASE_2_log ]
then
        ./detectexit.sh 2 &
fi

if [ -f data/DATABASE_3_log ]
then
        ./detectexit.sh 3 &
fi

if [ -f data/DATABASE_4_log ]
then
        ./detectexit.sh 4 &
fi

echo "Rebooted all exit listeners"
