#!/bin/bash
#this script automates some the requirements needed to install ceph
#this script is intended for use for the HPCCEA clusters specifically
#NOT for general use
#run this script as root on the management node

#install epel
for i in {1..5}
do
 ssh e$i -l root "yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm"
done

#update yum packages
yum update -y

#install ceph-deploy utility
yum install -y ceph-deploy

for i in {1..5}
do

  #install ntp and synchronize the time between all nodes
  #start the ntp daemon
  ssh e$i -l root "yum install -y ntp  ntpdate ntp-doc
                   ntpdate 0.us.pool.ntp.org
                   hwclock -w

                   if ( !(systemctl is-active ntpd) ); then
                     systemctl enable ntpd
                     systemctl start ntpd; fi"

  #check if ssh is running
  #if not install and start the ssh daemon
  ssh e$i -l root "if ( !(systemctl is-active sshd) ); then
                   yum install -y openssh-server
                   systemctl enable sshd
                   systemctl start sshd; fi"
done

unamedef=ceph-user
#prompt the user for the name of the ceph user
echo "Enter the desired username for the ceph user account and press [ENTER]"
read unamein

if [[ "$unamein" == "ceph" ]] ; then
  echo "username {ceph} reserved for daemon. Setting to default of ceph-user"
  unamein=$unamedef
fi

#create a ceph user (the user cannont be named 'ceph' as this is reserved for the c
#eph daemon)
#set the password to password (can be changed once the script has finished
useradd -d /home/$unamein -m $unamein -p password

#give the ceph user sudo permissions
echo "$unamein ALL = (root) NOPASSWD:ALL" | tee /etc/sudoers.d/$unamein
chmod 0440 /etc/sudoers.d/$unamein

#copy the passwd/shadow/gshadow/group files from the management node to the other n
#odes
for i in {2..5}
do
 scp /etc/shadow/ e$i:/etc/shadow
 scp /etc/gshadow e$i:/etc/gshadow
 scp /etc/group e$i:/etc/group
 scp /etc/passwd e$i:/etc/passwd
done
