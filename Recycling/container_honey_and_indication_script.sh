#!/bin/bash

containerName=$1

# install ssh on container
sudo lxc-attach -n $1 -- bash -c "sudo apt-get -qq update"
sudo lxc-attach -n $1 -- bash -c "sudo apt-get -qq install openssh-server"

# install snoopylogger if requested
if [[ $containerName == "DATABASE_2" ]] || [[ $containerName == "DATABASE_4" ]]
then
  sudo lxc-attach -n $containerName -- bash -c "sudo apt-get install wget -y"
  sudo lxc-attach -n $containerName -- bash -c "sudo wget -O install-snoopy.sh https://github.com/a2o/snoopy/raw/install/install/install-snoopy.sh"
  sudo lxc-attach -n $containerName -- bash -c "chmod 755 install-snoopy.sh"
  sudo lxc-attach -n $containerName -- bash -c "sudo ./install-snoopy.sh stable"
  sudo lxc-attach -n $containerName -- bash -c "rm -rf ./install-snoopy.* snoopy-*"
fi

# install ssh warning banner and place banner file inside container if requested
if [[ $containerName == "DATABASE_3" ]] || [[ $containerName == "DATABASE_4" ]]
then
  sudo cp ./ssh_banner_info/warning_banner /var/lib/lxc/$containerName/rootfs/etc/
  sudo lxc-attach -n $containerName -- bash -c "sudo mv /etc/warning_banner /etc/motd"
fi

sudo lxc-attach -n $containerName -- bash -c "cd /etc/ssh && sudo echo 'PermitRootLogin yes' >> sshd_config"
sudo lxc-attach -n $containerName -- bash -c "cd /etc/ssh && sudo echo 'MaxStartups 1' >> sshd_config"
sudo lxc-attach -n $containerName -- bash -c "sudo systemctl restart ssh"

# copy honey files over from honey folder on host
sudo lxc-attach -n $1 -- bash -c "cd / && cd home && sudo mkdir jerrym && cd jerrym && sudo mkdir Desktop && sudo mkdir Documents"
sudo cp -r ./honey/* /var/lib/lxc/$containerName/rootfs/home/jerrym/Documents/