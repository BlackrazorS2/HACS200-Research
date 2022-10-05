#!/bin/bash
# pass in honeypot number through argument

inotifywait -q -m -e close_write honeypot$1_log |
while read -r filename event; do
	if tail -1 "$filename" | grep -q "Attacker closed connection"; 
	then
		# copy the MITM logs to our data collection directory.
		# copy modified files to a private container for potential future analysis.
		./recycler.sh
	fi
done
