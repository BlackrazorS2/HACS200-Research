#!/bin/bash

# kills all detectexit scripts and restarts them

killall inotifywait

echo "Killed all exit listeners"

if [ -f DATABASE_1_log ]
then
        ./detectexit.sh 1 &
fi

if [ -f DATABASE_2_log ]
then
        ./detectexit.sh 2 &
fi

if [ -f DATABASE_3_log ]
then
        ./detectexit.sh 3 &
fi

if [ -f DATABASE_4_log ]
then
        ./detectexit.sh 4 &
fi

echo "Rebooted all exit listeners"