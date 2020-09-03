#!/bin/bash

CONTAINER="integrark"
REPOSITORY="https://github.com/knowark/integrark.git"
PLAYBOOK="setup/deploy.yml"
REPOSITORY_PATH=$(dirname $(echo $PWD))

echo $REPOSITORY_PATH
#echo "Deploying LXD container..."

#lxc launch ubuntu:focal $CONTAINER
#lxc config device add $CONTAINER home disk source=$HOME path=/mnt/$HOME

#echo "Install Ansible..."

#sleep 5  # Wait for container network connectivity.
#lxc exec $CONTAINER -- apt update -y
#lxc exec $CONTAINER -- apt install ansible -y
#lxc exec $CONTAINER -- apt autoremove -y

#echo "Deploy with Ansible Pull..."

#lxc exec $CONTAINER -- ln -s /mnt

##lxc exec $CONTAINER -- bash -c "ansible-pull -c local -i localhost, \
    ##-U $REPOSITORY -d /var/git/$CONTAINER $PLAYBOOK 2>&1 | tee deploy.log"
