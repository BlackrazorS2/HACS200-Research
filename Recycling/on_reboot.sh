sudo lxc-start -n DATABASE_1
sudo lxc-start -n DATABASE_2
sudo lxc-start -n DATABASE_3
sudo lxc-start -n DATABASE_4

sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_1_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_2_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_3_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_4_log

sudo modprobe br_netfilter
sudo sysctl -p /etc/sysctl.conf

sudo ./firewall_rules.sh

sudo killall inotifywait

sudo ./container_rotate.sh 1 0 1

#sudo ./restartdetect.sh