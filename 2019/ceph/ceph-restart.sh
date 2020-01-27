#!/bin/bash
#this script will allow the user to restart the ceph install process
#this script is intended for use for the HPCCEA clusters specifically
#NOT for general use

#check if ceph-deploy is installed
#delete all ceph data
if [[ $( rpm -qa ceph-deploy ) =~ $ceph-deploy ]]; then
  ceph-deploy purge e1 e2 e3 e4 e5
  ceph-deploy purgedata e1 e2 e3 e4 e5
  ceph-deploy forgetkeys
  sudo rm -rf ceph.*
fi
