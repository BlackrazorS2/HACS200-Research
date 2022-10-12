#!/bin/bash

# kills all detectexit scripts and restarts them

killall inotifywait

echo "Killed all exit listeners"

if [ -f honeypot1_log ]
then
	./detectexit.sh 1 &
fi

if [ -f honeypot2_log ]
then
	./detectexit.sh 2 &
fi

if [ -f honeypot3_log ]
then
	./detectexit.sh 3 &
fi

if [ -f honeypot4_log ] 
then
	./detectexit.sh 4 &
fi

echo "Rebooted all exit listeners"
