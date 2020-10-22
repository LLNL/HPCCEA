#!/bin/bash

###########################################
######## Initial node information #########
###########################################
CLUSTER_NAME=$1    # cluster name         #
MGMT_PUB_IP=$2     # management public IP #
MGMT_NET=$3        # Management network   #
IB_NET=$4          # IB network           #
IPMI_NET=$5        # IPMI network         #
ROOTPASS=$6        # Root Password        #
###########################################


##################################################
#### configure Ansible host file #################
##################################################
for i in {2..5}	   			         #
do					 	 #  
echo "e$CLUSTER_NAME$i" >> /etc/ansible/hosts    #
done					  	 #
echo "e${CLUSTER_NAME}i" >> /etc/ansible/hosts   #
##################################################
echo "[compute]" >> /etc/ansible/hosts     	 #
for i in {2..5}				  	 #
do					 	 #  
echo "e$CLUSTER_NAME$i" >> /etc/ansible/hosts    #
done					 	 #
##################################################
echo "[management]" >> /etc/ansible/hosts   	 #
echo "e${CLUSTER_NAME}i" >> /etc/ansible/hosts   #
##################################################

#package installs
ansible-playbook All_Packages_install.yml

#Setup the host file
bash Setup_hosts.sh ${CLUSTER_NAME} ${MGMT_PUB_IP} ${MGMT_NET} ${IB_NET} ${IPMI_NET}

#em1 setup
ansible-playbook em1.yml -e "em1=$MGMT_PUB_IP"

#network restart
systemctl restart network

#Setup to resolv.conf
ansible-playbook Resolv_Setup.yml

#tftpboot setup
ansible-playbook tftpboot_setup.yml

#Syslinux setup
ansible-playbook setup_syslinux.yml

#PXE setup
ansible-playbook Default_Setup.yml -e "mgmt_ip=$MGMT_NET"

#tftp configure and iso download
ansible-playbook tftp_populate.yml

#em2 setup
ansible-playbook em2.yml -e "em2=$MGMT_NET"

#DHCP setup
bash DHCP_Setup.sh ${MGMT_NET}

#Anaconda-ks file set up for compute nodes
ansible-playbook anaconda-ks.yml -e "mgmt_ip_address=$MGMT_NET root_password=$ROOTPASS" 

#Xinetd.d setup
bash xinetd.sh

#IPMI setup
ansible-playbook ipmi_install.yml -e "cluster_name=$CLUSTER_NAME em21=$IPMI_NET"

#Seting up route for compute nodes to access internet
ansible-playbook iptables.yml -e "mgmt_network=$MGMT_NET mgmt_ip=$MGMT_PUB_IP"

#infiniband
modprobe ib_ipoib
ansible-playbook mgmt_infiniband.yml -e "IB_IP=$IB_NET"

#Download RPM SETUP
bash rpms.sh 
