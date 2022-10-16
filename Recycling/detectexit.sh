#!/bin/bash
# pass in honeypot number through argument

inotifywait -q -m -e close_write data/DATABASE_$1_log |
while read -r filename event; do
        if tail -1 "$filename" | grep -q "Attacker closed connection";
        then
                honeypot_ip=$(sudo cat ./properties/DATABASE_$1_properties | cut -d' ' -f1)
                # copy the MITM logs to our data collection directory.
                # copy modified files to a private container for potential future analysis.
                ./recycler.sh DATABASE_$1 $honeypot_ip 1
        fi
done
