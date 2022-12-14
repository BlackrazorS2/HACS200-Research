#!/bin/bash

if [ $# -ne 3 ]
then
  echo "Usage ./recycler.sh [container name] [external IP] [create new container (1 for yes, 0 for no)]"
  exit 1
fi

# Retrieves the MITM port associated with honeypot
port=$(sudo cat ./properties/$1_properties | cut -d' ' -f2)
status=$(sudo lxc-ls | grep $1 | wc -l)

# Destroy resources if honeypot is up
if [ $status -ne 0 ]
then
  # Store back up of data
  sudo ./copy_data.sh $1
  
  # Destroy relevant IP table rules
  IP=$(sudo lxc-info -n $1 -iH)
  sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --jump DNAT --to-destination $IP
  sudo iptables -w --table nat --delete POSTROUTING --source $IP --destination 0.0.0.0/0 --jump SNAT --to-source $2
  sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 10.0.3.1:$port
 
  # Close MITM server
  sudo pm2 stop $1
  sudo pm2 delete $1
  sudo echo "IP:  $IP"
  sudo echo "destination: $2"

  #sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --jump DNAT --to-destination $IP
  #sudo iptables -w --table nat --delete POSTROUTING --source $IP --destination 0.0.0.0/0 --jump SNAT --to-source $2
  #sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 10.0.3.1:$port
  #sudo iptables --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 127.0.0.1:$port
  sudo ip addr delete $2/16 brd + dev enp4s2
  
  # Destroy honeypot container
  sudo lxc-stop -n $1
  sudo lxc-destroy -n $1
fi

if [ $3 -eq 1 ]
then
  # Create new container for honeypot
  sudo lxc-create -n $1 -t download -- -d ubuntu -r focal -a amd64
  sudo lxc-start -n $1
  sleep 5s
  
  # Populate container with correct indication of monitoring
  ./container_honey_and_indication_script.sh $1
  IP=$(sudo lxc-info -n $1 -iH)
  dirpath=$( dirname -- "$( readlink -f -- "$0"; )"; )
  logpath="$dirpath/data/$1_log"

  # Boot up MITM server
  sudo pm2 -l $logpath start /home/student/MITM/mitm.js --name $1 -- -n $1 -i $IP -p $port --mitm-ip 10.0.3.1 --auto-access --auto-access-fixed 1 --debug & echo "pid $!"

  container_num=4
  if [[ $1 == "DATABASE_1" ]]
  then
    container_num=1
  fi

  if [[ $1 == "DATABASE_2" ]]
  then
    container_num=2
  fi

  if [[ $1 == "DATABASE_3" ]]
  then
    container_num=3
  fi

  #sudo ./detectexit.sh $container_num &

  sleep 90s
  
  # Generate new IP table rules for honeypot
  sudo ip link set dev enp4s2 up
  sudo ip addr add $2/16 brd + dev enp4s2
  sudo iptables -w --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $2 --jump DNAT --to-destination $IP
  sudo iptables -w --table nat --insert POSTROUTING --source $IP --destination 0.0.0.0/0 --jump SNAT --to-source $2
  #sudo iptables --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 127.0.0.1:$port
  sudo iptables -w --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 10.0.3.1:$port
  sudo sysctl -w net.ipv4.conf.all.route_localnet=1
fi
exit 0
