#!/bin/bash

# Simple script for CentOS 7 Guest creation

virt-install --name centos7_mod \
--ram 1024 \
--vcpus=2 \
--os-variant=centos7.0 \
--nographics \
--disk path=/var/lib/libvirt/images/centos7_mod.qcow2,size=8,bus=virtio,format=qcow2 \
--location=/var/lib/libvirt/boot/CentOS-7-x86_64-DVD-2003.iso  \
--network "bridge=br1" \
--initrd-inject=/var/lib/libvirt/boot/centos7_mod.ks \
--extra-args "console=ttyS0 ks=file:/centos7_mod.ks"
