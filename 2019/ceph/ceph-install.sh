#!/bin/bash
#this script automates a few steps of the ceph install process
#this script is intended for use for the HPCCEA clusters specifically
#NOT for general use
#run this script from the ceph user account on the management node

#get the number of nodes
echo "Enter the number of nodes and then press [ENTER]"
read numnodes

nodes=$(($numnodes+1))

#make sure ceph-deploy is installed
if ! [[ $(rpm -qa ceph-deploy ) =~ $ceph-deploy ]]; then
  sudo yum install -y ceph-deploy
fi



#prompt the user for the name of the node they want to use
#as the monitor node
echo "Enter the name of the node to use as the monitor node"
echo "ie {exenon2} then press [ENTER]"
read monnode

#create the monitor node
sudo ceph-deploy new $monnode

#get the hostnames of the cluster aliases
hostname=$( cat /etc/hostname )

#needed for clusters whos managment node hostname ends in an 'i'
if [[ "${hostname: -1}" == i ]]; then
  hostname="${hostname::-1}"
fi

#install ceph on all nodes except management node
for i in $( seq 2 $nodes ); do
  sudo ceph-deploy install $hostname$i
done

#deploy the monitor and gather the keys
sudo ceph-deploy mon create-initial

#copy the configuration file from the admin/management node to all other nodes
for i in $( seq 2 $nodes ); do
  sudo ceph-deploy admin $hostname$i
done

#prompt the user and ask which nodes they want to use as storage nodes
echo "Enter the names of the two nodes that you would like to use as OSD nodes separated by spaces"
echo "OSD is ceph's Object Storage Daemon and these nodes will be used for storing data"
echo "Press [ENTER] when done"

#get the OSD node names
read osd1 osd2

#install the manager daemon on the OSD nodes
sudo ceph-deploy mgr create $osd1 $osd2

