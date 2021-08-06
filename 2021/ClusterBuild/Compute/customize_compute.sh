#!/bin/bash

# Assumptions

# Customization of management node has been completed

# passwordless ssh needs to have been setup

# set environment variable USERPW before runnint script to password is not in the repo


# Setup user accounts and ssh access
ansible-playbook root_ssh.yml -e 'username=test1 upassword=${USERPW} userid=5001'

#Sets up host file
ansible-playbook setup_hostfile.yml

#Sets up iptables
ansible-playbook setup_iptables.yml

#Sets up IB
ansible-galaxy collection install ansible.posix
ansible-playbook IB_setup.yml

# install packages
ansible-playbook package_install.yml

# Install community General and Pdsh
ansible-galaxy collection install community.general
ansible-playbook pdsh.yml

#Sets up mpi
ansible-playbook mpifile.yml

#Sets up chrony
ansible-playbook install_chrony.yml

#Sets up slurm and munge
ansible-playbook install_slmu.yml
rm -rf /etc/munge/munge.key
ansible-playbook install_slmu_2.yml
ansible-playbook configure_slurm.yml -e "lead=nickel"  ## todo fix so playbook figures out variable name

#Sets up nfs
ansible-playbook nfs.yml

#Sets up Cron 
ansible-playbook setup_cron.yml

#Updates Centos - breaks our IB driver run manually and update IB driver at the same time
#ansible-playbook updates.yml
