virt-install --name opensuseks --os-variant=linux --disk path=/var/lib/libvirt//images/opensuseks.qcow,size=8,format=qcow2,bus=virtio --nographics --vcpus=2 --ram=1024 --network "bridge=br1" --location=/var/lib/libvirt/boot/openSUSE-Leap-15.2-DVD-x86_64-Current.iso -x "autoyast=file:/root/kvm_project/openSUSE/autoinst.xml" --extra-args "console=ttyS0"

