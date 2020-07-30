#!/bin/bash

# Script to configure a compute node after it is installed via kickstart

export IBNAME=stc2
export TARGETNODE=e$IBNAME
export MGMTNODE=estci 

# setup ntp
ansible-playbook ntp_setup.yaml --limit $TARGETNODE

# install repo for slurm and munge
ansible-playbook cluster-repo.yaml 

export emgmt=$MGMTNODE
# now create repo file  with variables defined above
envsubst < slurm-munge.repo.tmpl  > slurm-munge.repo
ansible-playbook cpcluster-repo.yaml --limit $TARGETNODE
rm slurm-munge.repo

# create a user
# $1 = password for test user
# $2 = user and group ID for test user (they are the same number)
./create-users.sh testuser $1 $2 $2 $TARGETNODE $MGMTNODE

# install IB and mpi and setup interface
ansible-playbook infiniband_package_install.yml --limit $TARGETNODE
ansible-playbook openMPI_install.yml --limit $TARGETNODE

IBIP=$(getent hosts $IBNAME | awk '{print $1}')
ansible-playbook mkib0.yaml -e ip_addr="$IBIP" --limit $TARGETNODE

# install slurm
./installslrum.sh

# comfigure limits
ansible-playbook memlock.yml --limit $TARGETNODE

# setup nfs
./nfs_setup.sh  $TARGETNODE

# update node
ansible-playbook yumupdate.yml --limit $TARGETNODE

# reboot node
ansible-playbook reboot.yml --limit $TARGETNODE
