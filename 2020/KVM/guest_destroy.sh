#!/bin/bash

# Simple script to destroy and undefine guests because I got tired of running three commands.
# Please run as root or use sudo.

if [ $# -ne 1 ]; then
  echo "Invalid # of args. Please specify guest to be destroyed."
  exit 1
fi

virsh destroy $1
virsh undefine $1
rm -f /var/lib/libvirt/images/$1.qcow2
