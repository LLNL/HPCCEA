# Install a Lustre Cluster Using a ZFS Backend On 3 Centos

# 7.9 KVMs

## Part 1: Installing the Centos 7.9 KVMs

We asume you already installed libvirt and configured the software to run vms. We will cover how to create new vms for the lustre cluster.

Download centos 7.9 and put it in the directory for libvirt.

```
cd /var/lib/libvirt/boot/
wget http://mirrors.ocf.berkeley.edu/centos/7.9.2009/isos/x86_64/CentOS-7-x86_64-DVD-2009.iso
```
Create the kickstart file for the vm in /var/lib/libvirt/boot/c7.ks

Note: Replace "<VM_PASSWORD>" with whatever password you want to use to log in to the vms. Also replace "<PASSWORD>".

```
auth --enableshadow --passalgo=sha
cdrom
firewall --disabled
text
firstboot --enable
ignoredisk --only-use=vda
keyboard --vckeymap=us --xlayouts=''
lang en_US.UTF-
selinux --disabled
network --bootproto=dhcp --device=eth0 --onboot=off --ipv6=auto --no-activate
# Root password
rootpw --plaintext <VM_PASSWORD>
services --enabled="chronyd"
# Do not configure the X Window System
skipx
# System timezone
timezone US/Pacific --isUtc
user --groups=wheel --name=dev --uid=1000 --
password --plaintext <PASSWORD> 
bootloader --append=" crashkernel=auto" --location=mbr --boot-drive=vda
autopart --type=lvm
clearpart --all --initlabel --drives=vda
%packages
@core
chrony
kexec-tools
%end
%addon com_redhat_kdump --enable --reserve-mb='auto'
%end
#sed -i 's/# %wheel.*ALL=(ALL).*NOPASSWD:.*ALL/%wheel\tALL=(ALL)\tNOPASSWD: ALL/' /etc/sudoers
%anaconda
pwpolicy root --minlen=6 --minquality=1 --notstrict --nochanges --notempty
pwpolicy user --minlen=6 --minquality=1 --notstrict --nochanges --emptyok
pwpolicy luks --minlen=6 --minquality=1 --notstrict --nochanges --notempty
%end
```

You will want your vms to have a static ip address. If you are using a dhcp server to assign entries for the virtual machines, you need to add them to the
dhcpd.conf and /etc/hosts files and restart the dhcp server (systemctl restart dhcpd):

(You can also assign your 3 vms ips statically and with these hostnames instead. All that matters is that they have a static ip address)

```
Hostname Mac address IP
```
```
lustre_mgs_mdt 52:54:00:00:21:01 192.168.95.41
```
```
lustre_oss1 52:54:00:00:21:02 192.168.95.42
```
```
lustre_client 52:54:00:00:21:03 192.168.95.43
```
Note: These values are arbitrary. You just need to be consistent.

Create the management node for the MGS/ MDT components:

```
export VM_NAME=lustre_mgs_mdt
export VM_MAC="52:54:00:00:21:01"
virt-install --name $VM_NAME --ram 2048 --vcpus=2 \
--os-variant=centos7.0 \
--location=/var/lib/libvirt/boot/CentOS-7-x86_64-DVD-2009.iso --nographics \
--disk path=/var/lib/libvirt/images/${VM_NAME}.qcow2,size=8,bus=virtio,format=qcow2 \
--disk path=/var/lib/libvirt/images/${VM_NAME}_disk.qcow2,size=2.5,bus=virtio,format=qcow2 \
--disk path=/var/lib/libvirt/images/${VM_NAME}_disk2.qcow2,size=2.5,bus=virtio,format=qcow2 \
--network "bridge=br1,mac=${VM_MAC}" --initrd-inject=/var/lib/libvirt/boot/lc7.ks \
--extra-args="console=ttyS0,115200n8 ks=file://lc7.ks"
```
Create the OSS/ OST vm:

```
export VM_NAME=lustre_oss
export VM_MAC="52:54:00:00:21:02"
virt-install --name $VM_NAME --ram 2048 --vcpus=2 \
--os-variant=centos7.0 \
--location=/var/lib/libvirt/boot/CentOS-7-x86_64-DVD-2009.iso --nographics \
--disk path=/var/lib/libvirt/images/${VM_NAME}.qcow2,size=8,bus=virtio,format=qcow2 \
--disk path=/var/lib/libvirt/images/${VM_NAME}_disk.qcow2,size=5,bus=virtio,format=qcow2 \
--network "bridge=br1,mac=${VM_MAC}" --initrd-inject=/var/lib/libvirt/boot/lc7.ks \
--extra-args="console=ttyS0,115200n8 ks=file://lc7.ks"
```
Create the client vm:

```
export VM_NAME=lustre_client
export VM_MAC="52:54:00:00:21:03"
virt-install --name $VM_NAME --ram 2048 --vcpus=2 \
--os-variant=centos7.0 \
--location=/var/lib/libvirt/boot/CentOS-7-x86_64-DVD-2009.iso --nographics \
--disk path=/var/lib/libvirt/images/${VM_NAME}.qcow2,size=8,bus=virtio,format=qcow2 \
--network "bridge=br1,mac=${VM_MAC}" --initrd-inject=/var/lib/libvirt/boot/lc7.ks \
--extra-args="console=ttyS0,115200n8 ks=file://lc7.ks"
```
## Part 2: Building Lustre / ZFS from source

To install the lustre components, we will compile the rpms on the management node and copy the needed rpms to the other vms.

On each vm, clone the lustre and zfs and install the necessary packages.


```
cd
yum install -y epel-release
yum install -y git libtool flex bison kernel kernel-devel zlib-devel libuuid-devel \
libblkid-devel libtirpc-devel openssl-devel make rpm-build ncompress \
libaio-devel libattr-devel libffi-devel libudev-devel python36-cffi \
python36-packaging python3-devel libmount-devel libyaml-devel libnl3-devel
git clone https://github.com/lustre/lustre-release
git clone https://github.com/openzfs/zfs
#Reboot the machine to use the new kernel
reboot
```
Building the ZFS RPMS on the MGS/MDT and OSS nodes:

(Replace the "<kernel_directory>" with the directory to the kernel you plan to use.)

```
cd zfs
chmod +x autogen.sh
./autogen.sh
./configure --with-spec=redhat --with-linux=/usr/src/kernels/<kernel_directory>
make rpms
mkdir ~/zfs-rpms
mv *.rpm ~/zfs-rpms
```
Build the lustre client RPMS on the Client vm:

(Replace the "<kernel_directory>" with the directory to the kernel you plan to use.)

```
cd
cd lustre-release
chmod +x autogen.sh
./autogen.sh
./configure --with-spec=redhat --with-linux=/usr/src/kernels/<kernel_directory>
make rpms
mkdir ~/lustre-client-rpms
mv *.rpm ~/lustre-client-rpms
```
Build the lustre server RPMS on the MGS/MDT and OSS nodes:

(Replace the "<kernel_directory>" with the directory to the kernel you plan to use.)

```
cd
cd lustre-release
chmod +x autogen.sh
./autogen.sh
./configure --with-spec=redhat --with-linux=/usr/src/kernels/<kernel_directory> --enable-server
make rpms
mkdir ~/lustre-server-rpms
mv *.rpm ~/lustre-server-rpms
```
## Part 3: Installing Lustre / ZFS

Now that we have three folders containing the zfs, lustre client, and lustre server rpms, we can install them.

On the MDS/MDT and OSS/OST vms, install the zfs and lustre server RPMS. (Make sure not to install the kmod and dkms packages together. We
installed the kmod packages, not the dkms.)

```
yum install -y ~/zfs-rpms/*.rpm
yum install -y ~/lustre-server-rpms/*.rpm
```

On the client, install the client RPMS.

```
yum install -y ~/lustre-client-rpms/*.rpm
```
## Part 4: Edit /etc/ldev.conf

Context: The /etc/ldev.conf is the configuration file for lustre devices. You will need to tell the system of the OST, MDT, and MGS.

Copy this content to your /etc/ldev.conf file on the MGS and OSS servers. The client can have this file too, but it's unnecessary.
You'll need to replace the <lustre_X_hostname> with the actual hostname corresponding with your MGS/MDT and OSS servers. For example change
<lustre_mgs_vm_hostname> to lustre_mgs_mdt.

Note: MGS and MDT are on the same vm in this case.

```
#hostname [failover]/- label [md|zfs:]device-path
<lustre_mgs_vm_hostname> - mgs zfs:lustre-mgs/mgs
# Example: lustre_mgs_mdt - mgs zfs:lustre-mgs/mgs
<lustre_mdt_vm_hostname> - mdt zfs:lustre-mdt0/mdt
# Example: lustre_mgs_mdt - mdt zfs:lustre-mdt0/mdt
<lustre_ost0_hostname> - ost0 zfs:lustre-ost0/ost
# Example: lustre_oss - ost0 zfs:lustre-ost0/ost
```
## Part 5: Set Up the Lustre FS

*Note: Use lsblk command to view which disks are available. (i.e. /dev/vdb) and replace <DISK> with the actual disk name.

1. Create the MGS on the MGS vm

```
mkfs.lustre --mgs --backfstype=zfs --fsname=lustre lustre-mgs/mgs /dev/<DISK>
# Example: mkfs.lustre --mgs --backfstype=zfs --fsname=lustre lustre-mgs/mgs /dev/vdb
```
2. Create the MDT on the same MGS vm

```
mkfs.lustre --mdt --backfstype=zfs --fsname=lustre --index=0 --mgsnode=<MGS_VM_IP_ADDR>@tcp0 lustre-mdt0/mdt
/dev/<OTHER_DISK>
# Example: mkfs.lustre --mdt --backfstype=zfs --fsname=lustre --index=0 --mgsnode=192.168.95.41@tcp0 lustre-mdt
/mdt0 /dev/vdc
```
3. Create the OST on the OSS vm

```
mkfs.lustre --ost --backfstype=zfs --fsname=lustre --index=1 --mgsnode=<MGS_VM_IP_ADDR>@tcp0 lustre-ost0/ost
/dev/<DISK>
# Example: mkfs.lustre --ost --backfstype=zfs --fsname=lustre --index=1 --mgsnode=192.168.95.41@tcp0 lustre-ost
/ost0 /dev/vdb
```
Remember to put them all on the same network (i.e. tcp0) before you create them.

Now verify that the memory pools were created:

```
zpool list
```
You should see the memory pools you specified. If you dont, you can retry with the same command. Just add --reformat option.


## Part 6: Set Up the LNET (Lustre Network)

Context: LNET is the network the lustre devices use to communicate with each other.

Configure LNET on each vm (Client, MGS/MDT, OSS) and add each vm's own NID (Network ID) to the LNET

```
modprobe lnet #Check if the lnet kernel module is present
lnetctl lnet configure --all # Add own NID to the network
lctl list_nids # Verify that NID is added
# If nothing is listed, try this: lnetctl net add --net tcp0 --if eth
```
Now we need to add the peers to each vm:

```
lnetctl peer add --prim_nid <IP_OF_PEER>@tcp
# Example for the MGS/MDT vm:
# Add the OSS as a peer: lnetctl peer add --prim_nid 192.168.95.42@tcp
# Add the Client as a peer: lnetctl peer add --prim_nid 192.168.95.43@tcp
# Add self as a peer: lnetctl peer add --prim_nid 192.168.95.41@tcp
```
```
The MGS/MDT vm will need to become peers with the OST/OSS vm, the Client, and itself.
The OSS/OST vm will need to become peers with the MGS/MDT vm.
The Client will need to be peers with the MGS/MDT vm.
```
Verify the node and its peers are present:

```
lnetctl peer list
```
## Part 7: Mount the Lustre Servers

Now we should be able to mount each server node. Make sure you substitute the <device_path> with the corresponding device_path in your /etc/ldev.conf.

Make sure lustre is installed and running:

```
modprobe zfs
modprobe lustre
systemctl start lustre
systemctl status lustre
```
Mount the MGS and MDT on the MGS/MDT vm:

```
mkdir -p /mnt/lustre/mdt
mount -t lustre <mdt_device_path> /mnt/lustre/mdt
# Example: mount -t lustre lustre-mdt0/mdt0 /mnt/lustre/mdt #MDT
```
Do this on the same MGS/MDT vm as well:

```
mkdir -p /mnt/lustre/mgs
mount -t lustre <mgs_device_path> /mnt/lustre/mgs
# Example: mount -t lustre lustre-mgs/mgs /mnt/lustre/mgs #MGS
```
Mount the OST on the OSS vm:

```
mkdir /mnt/lustre/
mount -t lustre <ost_device_path> /mnt/lustre/
# Example: mount -t lustre lustre-ost0/ost0 /mnt/lustre/
```

## Part 8: Mount the Client

Once you have your Management Server and OSS set up, mount the client to the filesystem

```
mount -t lustre <MGS_NODE_IP_ADDR>@tcp0:/lustre /mnt/
# Example: mount -t lustre 192.168.95.41@tcp0:/lustre /mnt/
```
### Trouble Shooting


- Run into issues with the kernel-devel? Try:
yum install kernel-devel # Update kernel-devel
yum install -y "kernel-devel-uname-r == $(uname -r )" # Installs the kernel-devel for your distro

- Did you start lustre before adding the vm to the network (lnet) and after disabling the firewall daemon?

- Did you just make lustre, or did you make the rpms too? (ls *rpm in ~/lustre-release/ dir and check. If not, make them with "make rpms")

- Lustre not starting? You may not have lnet configured properly or have not done mkfs.lustre properly.
If the mgs and mdt are on the same node: You need to partition the disk /dev/vd*, (ie /dev/vdb) or else mkfs.lustre will use the entire disk for only
one of these. Another option is to create an extra disk upon creation of the VM.

- For lnet: Are all NIDs added to the network using the same tcp number? For example, lnetctl add mgs@tcp1 & lnetctl add ost@tcp2 will not work.
They both need to have the same tcp number (both 1 or both 2).
Check with "lnetctl peer show"

- Did you format the disks properly with mkfs.lustre?
Check if the number after "tcp" is the same for the mgs,mdt, and ost.
Check if the command corresponds with your /etc/ldev.conf file.
If you found you've made a mistake reformat it with the --reformat flag: https://linux.die.net/man/8/mkfs

- Lustre not starting? A possible reason for this may be that the index number may be taken. If you see something like this in /var/log/messages:

#### ```

```
Aug 9 12:04:39 nvm6 kernel: LustreError: 140-5: Server lustre-OST0001 requested index 1, but that index
is already in use. Use --writeconf to force
Aug 9 12:04:39 nvm6 kernel: LustreError: 2822:0:(mgs_handler.c:503:mgs_target_reg()) Failed to write
lustre-OST0001 log (-98)
Aug 9 12:05:40 nvm6 kernel: LustreError: 140-5: Server lustre-OST0001 requested index 1, but that index
is already in use. Use --writeconf to force
Aug 9 12:05:40 nvm6 kernel: LustreError: 2824:0:(mgs_handler.c:503:mgs_target_reg()) Failed to write
lustre-OST0001 log (-98)
```

Then go back to part three and use a different index number that is not in use.
Try checking /var/logs/messages for any other hints.
- You can also run:
```
lctl dk <filename>
```

to view debug logs on each of the vms.

- For more help with troubleshooting, visit https://www.lustre.org/documentation/
and navigate to Part V. Troubleshooting a Lustre File System.

Sources:


- https://wiki.lustre.org/Lustre_with_ZFS_Install#Build_ZFS
- https://wiki.lustre.org/KVM_Quick_Start_Guide
- https://wiki.whamcloud.com/pages/viewpage.action?pageId=


