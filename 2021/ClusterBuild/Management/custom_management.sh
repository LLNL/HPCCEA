#!/bin/bash

# Assumptions
# ssh keys already created on mgmt node
# ansible package installed
#   dnf install -y centos-release-ansible-29.noarch  ## may require default route, resolv.conf
#   yum install ansible
# /etc/ansible/hosts - needs to be populated
#   [management]
#   e1
#
#   [compute]
#   e2
#   e3

# manually add mgmt ethernet - then setup  passwordless ssh to nodes

# assume file /root/CentOS-8.3.2011-x86_64-dvd1.iso exists

# assume dd-megaraid_sas-07.714.04.00-1.el8_3.elrepo.iso  and dd-mlx4-4.0-4.el8_3.elrepo.iso 
#   are already downloaded
 
# Define the ROOTPW varialbe at the shell before running so the root password is not pushed into the repo

# The file address_dict.yml must be up to date with the names and MAC addrs of nodes int he cluster


# TODO - change these to be ansible variables in an ansible variables file

# Define clustername in CLUSTERNAME variable
# Define network values to be used in the cluster
#   NUMNODES, OUTWARDIP, ETHOCT,  IPMIOCT, IBOCT, EXTOCT - TODO coalesce OUTWARDIP and EXTIP

export CLUSTERNAME=nickel
export NUMNODES=3
export OUTWARDIP=59.7
export ETHOCT=95
export MGMTIP=192.168.95.1
export IPMIOCT=96
export IBOCT=129
export EXTIP=192.168.59.7


ansible-playbook set-hostname.yml --extra-vars "host=${CLUSTERNAME}"

#Creates hostfile
ansible-playbook add_hosts.yml --extra-vars "host=${CLUSTERNAME} nodes=${NUMNODES} outward_ip=${OUTWARDIP} eip=${ETHOCT} pip=${IPMIOCT} hip=${IBOCT}"

#Auto accept ssh key for e1 (mgmt node interface) now that it has been configured
ssh -o StrictHostKeyChecking=no e1 hostname 

#Sets up the Network
ansible-playbook setup_networkscripts.yml --extra-vars "cluster_name=${CLUSTERNAME}i hip=${IBOCT}"

ifup eno2
ifup ib0

#Creates resolv.conf
ansible-playbook add_resolv.yml

# Install additional packages
ansible-playbook package_install.yml

#installs additional packages for ansible.
ansible-galaxy collection install community.general
ansible-galaxy collection install ansible.posix

#Setup syslinux.
### Note different hardward type use ttyS0 or ttyS1 - make that a cluster related variable
ansible-playbook syslinux.yml -e "ipaddr=${EXTIP}"

#Mount iso.
ansible-playbook mountcentos.yml
#Sets up httpd.
ansible-playbook httpd.yml

#Sets up dhcpd.
ansible-playbook dhcp.yml

#Sets up xinetd.
ansible-playbook xinetdFile.yml

#disables firewall.
ansible-playbook firewall.yml

#Fix perms for selinux.
ansible-playbook fix_selinux.yml

#Sets up kickstart file.
ansible-playbook setup_kickstart.yml -e "mgmt_ip=${MGMTIP} root_password=${ROOTPW}"

