#!/bin/bash
# pass in honeypot number through argument

sudo inotifywait -q -m -e modify data/DATABASE_$1_log |
while read -r filename event; do
        if tail -1 "$filename" | grep -q "Attacker closed connection";
        then
                echo "honeypot $1 attacker exit"
                honeypot_ip=$(sudo cat ./properties/DATABASE_$1_properties | cut -d' ' -f1)
                # copy the MITM logs to our data collection directory.
                # copy modified files to a private container for potential future analysis.
                sudo ./recycler.sh DATABASE_$1 $honeypot_ip 1
        fi
done
