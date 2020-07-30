#!/bin/bash

# use the HOSTNAME environment variable (ie xenoni, boroni) of the mgmt node
# to create slurm.conf to push to nodes


export control_name=$HOSTNAME
export actual_name=e$HOSTNAME
export cluster_name=${HOSTNAME::-1}

# now create slurm.conf with variables defined above
envsubst < slurm.tmpl  > slurm.conf 

# now run the slurmsetup playbook 
ansible-playbook slurmsetup.yaml

# remove generated slurm.conf
rm -f slurm.conf
