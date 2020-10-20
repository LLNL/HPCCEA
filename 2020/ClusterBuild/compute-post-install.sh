#!/bin/bash

# Script to configure a compute node after it is installed via kickstart
#
# $1 = password for test user
# $2 = uid/gid - assumes uid and gid are the same number

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <password> <uid/gid (one number)> " >&2
  exit 1
fi

export IBNAME=stc2
export TARGETNODE=e$IBNAME
export MGMTNODE=estci 
export CLUSTERNAME=${MGMTNODE:1:-1}

# setup ntp
ansible-playbook ntp_setup.yaml --limit $TARGETNODE

# install repo for slurm and munge on mgmt node
ansible-playbook cluster-repo.yaml --limit $MGMTNODE

export emgmt=$MGMTNODE
# now create repo file  with variables defined above
envsubst < slurm-munge.repo.tmpl  > slurm-munge.repo
ansible-playbook cpcluster-repo.yaml --limit $TARGETNODE
rm slurm-munge.repo

# create a user
# $1 = password for test user
# $2 = user and group ID for test user (they are the same number)
bash ./create-users.sh testuser $1 $2 $2 $TARGETNODE $MGMTNODE

# install IB and mpi and setup interface
ansible-playbook infiniband_package_install.yml --limit $TARGETNODE
ansible-playbook openMPI_install.yml --limit $TARGETNODE

IBIP=$(getent hosts $IBNAME | awk '{print $1}')
ansible-playbook mkib0.yaml -e ip_addr="$IBIP" --limit $TARGETNODE


# variables for slurm setup
export control_name=${CLUSTERNAME}i
export actual_name=$MGMTNODE
export cluster_name=$CLUSTERNAME

# now create slurm.conf with variables defined above
envsubst < slurm.tmpl  > slurm.conf

# now run the slurmsetup playbook 
ansible-playbook slurmsetup.yaml --limit $MGMTNODE
ansible-playbook slurmsetup.yaml --limit $TARGETNODE

# remove generated slurm.conf
rm -f slurm.conf


# comfigure limits
ansible-playbook memlock.yml --limit $TARGETNODE

# setup nfs
bash ./nfs_setup.sh  $TARGETNODE

# update node
ansible-playbook yumupdate.yml --limit $TARGETNODE

# reboot node
ansible-playbook reboot.yml --limit $TARGETNODE
