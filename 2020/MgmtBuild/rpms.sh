#!/bin/bash

#Download Munge and Slurm
wget --quiet https://github.com/dun/munge/releases/download/munge-0.5.13/munge-0.5.13.tar.xz
wget --quiet https://download.schedmd.com/slurm/slurm-18.08.6-2.tar.bz2

#Build the RPM for munge
rpmbuild -ta --quiet munge-0.5.13.tar.xz

#Start the RPM for munge
rpm -ivh --quiet /root/rpmbuild/RPMS/x86_64/munge-*

#Build the RPM for munge
rpmbuild -ta --quiet slurm-18.08.6-2.tar.bz2

#Start the RPM for munge
rpm -ivh --quiet /root/rpmbuild/RPMS/x86_64/slurm-*

#Make Slurm directories
useradd -r -s /sbin/nologin slurm
mkdir /var/spool/slurm
chown slurm:slurm /var/spool/slurm

#Remove Munge and Slurm download removal
rm -rf munge-0.5.13.tar.xz
rm -rf slurm-18.08.6-2.tar.bz2
