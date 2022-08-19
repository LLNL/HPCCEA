#!/bin/bash

# this script will run after compute nodes are installed
# Assumes the root ssh key has been setup on each node so ansible can run (setup in kickstart)
#
# export INITIALUPASS=<password for initial user>

# set mgmt node to NAT for compute nodes
ansible-playbook ip_tables_config.yml

# install rpms on mgmt and compute nodes
ansible-playbook installComputePackages.yml

# create initial user
ansible-playbook create_account.yml

# note fix vars file
ansible-playbook ibconfig.yml

# setup mpi
ansible-playbook mpish.yml

# setup /etc/hosts
ansible-playbook create_hosts.yml

# setup chrony
ansible-playbook setupchrony.yml 

# setup munge
ansible-playbook setupmunge.yaml

#add local repo
ansible-playbook add_local_repo.yaml

# install slurm
ansible-playbook installSlurm.yml

# setup NFS
ansible-playbook nfs.yml
