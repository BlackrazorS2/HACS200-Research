sudo lxc-start -n DATABASE_1
sudo lxc-start -n DATABASE_2
sudo lxc-start -n DATABASE_3
sudo lxc-start -n DATABASE_4

sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_1_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_2_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_3_log
sudo echo "HOST REBOOTED, CONTAINER RECYCLED" >> ./data/DATABASE_4_log

sudo ./container_rotate 1 0 1

sudo ./restartdetect.sh