#!/bin/bash

if [ $# -ne 2 ]
then
  echo "Usage ./recycler.sh [container name] [external IP]"
  exit 1
fi
port=$(cat ~/properties/$1_properties | cut -d' ' -f2)
status=$(sudo lxc-ls | grep $1 | wc -l)

if [ $status -ne 0 ]
then
  IP=$(sudo lxc-info -n $1 -iH)
  sudo forever stop $1
  sudo iptables --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --jump DNAT --to-destination $IP
  sudo iptables --table nat --delete POSTROUTING --source $IP --destination 0.0.0.0/0 --jump SNAT --to-source $2
  sudo iptables --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 127.0.0.1:$port
  sudo ip addr delete $2/16 brd + dev enp4s2
  sudo lxc-stop -n $1
  sudo lxc-destroy -n $1
fi

sudo lxc-create -n $1 -t download -- -d ubuntu -r focal -a amd64
sudo lxc-start -n $1

sleep 5s
./container_honey_and_indication_script.sh $1
IP=$(sudo lxc-info -n $1 -iH)
sudo forever -l /home/student/data/$1_log --id $1 -a start /home/student/MITM/mitm.js -n $1 -i $IP -p $port --auto-access --auto-access-fixed 3 --debug & echo "pid $!"

sudo ip link set dev enp4s2 up
sudo ip addr add $2/16 brd + dev enp4s2
sudo iptables --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $2 --jump DNAT --to-destination $IP
sudo iptables --table nat --insert POSTROUTING --source $IP --destination 0.0.0.0/0 --jump SNAT --to-source $2
sudo iptables --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $2 --protocol tcp --dport 22 --jump DNAT --to-destination 127.0.0.1:$port
sudo sysctl -w net.ipv4.conf.all.route_localnet=1

exit 0
