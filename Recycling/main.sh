#!/bin/bash

sudo modprobe br_netfilter
sudo sysctl -p /etc/sysctl.conf

sudo ./firewall_rules.sh
sudo ./container_rotate.sh 0 0 1
#sudo ./restartdetect.sh