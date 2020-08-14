virt-install --name ctest --ram 1024 --vcpus=2 --os-variant=centos7.0 --location=/var/lib/libvirt/boot/CentOS-7-x86_64-DVD-2003.iso --nographics --network '"bridge=br1"' --disk path=/var/lib/libvirt/images/ctest.qcow2,size=8,bus=virtio,format=qcow2 --extra-args="console=ttyS0"


