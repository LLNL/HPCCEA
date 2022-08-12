#!/bin/bash

# prereq: 
#   - Install ansible (dnf install -y epel-release; dnf config-manager --enable epel; dnf install -y ansible)
#   - setup /etc/ansible/hosts for your cluster
#   [management]
#   oxygeni
#   [compute]
#   e[2:5]
#
#   - setup passwordless ssh  
#      ssh-keygen 
#      cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
#
#   - copy over or clone repo (may need to install git) the cd into top level
# 
#   - copy over prebuilt RPMS and put int /root/rpmbuild
#     cp -r rpmbuild /root/
#   
#   - Set the KSPASS environment variable for the password that Kickstart will use on compute nodes
#     ie - export KSPASS=<password to use>

# Note update variable file as appropriate or your cluster
# hosts_vars.yml

# create the host file
ansible-playbook create_hosts.yml
ansible-playbook hostname.yml

# create resolv.conf
ansible-playbook create_resolveconf.yml

# setup ethernet interface
ansible-playbook ethernet_config.yml 

# setup /tftboot file system
# note assumes disk is not already in use for something
# suggest wipefs -af /dev/sdb
ansible-playbook second_partition.yml

# download and install package and drivers
ansible-playbook packages-and-drivers.yml

# setup /tftpboot
ansible-playbook tftpplaybook.yml

# setup and copy files from ISO image
ansible-playbook isoimageplaybook.yml

# setup alma8 install folder
ansible-playbook setup-alma8-http-install.yml

# start httpd server
ansible-playbook starthttpd.yaml

# setup dhcp 
ansible-playbook configdhcp.yml

# disable firewall
ansible-playbook  firewall.yml

# setup tftp perms
ansible-playbook tftp-permissions.yml

# setup kickstart
ansible-playbook kickstart_setup.yml

# setup tftp SELinux perms
ansible-playbook tftp-permissions.yml


# setup yum repo
ansible-playbook createRepo.yml

## Note setup conman/powerman yum repo is pre-req
ansible-playbook install-conman-powerman.yaml
ansible-playbook powermanplaybook.yml
ansible-playbook conman.yml
