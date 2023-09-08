**How to Install Alma8 KVM on a node**

NOTE: This is How you would create an additional node and does not tell the user how to install the kvm application.

First, update `/etc/hosts` and `/etc/dhcp/dhcpd.conf`

	Do this for each VM you want to create
	
	On the management Node and Node you are running the VM on:
	Edit /etc/hosts:
	192.168.95.xx almaxx

	Do this only on the management node
	edit /etc/dhcp/dhcpd.conf
	
	host almaxx { 
		          hardware ethernet 52:54:00:00:95:77; #Note the MAC add can be whatever youd like
		          fixed-address 192.168.95.xx; #Make sure to use the same IP address as the /etc/hosts
		          option host-name :almaxx:;
		          filename "/pxelinux.0";
		        }
    restart dhcpd after 

		
  

**On the Compute Node:**

*    cd into `/var/lib/libvirt/boot`
*   create a file called "alma8.ks" and add these contents. Edit line 6 to the correct IP of the compute node. Additionally, edit the password on line 19 if you want.


		#version=RHEL8
		reboot
		cdrom
		eula --agreed
		text --non-interactive
		logging --level=debug --host=192.168.95.5--port=514 #EDIT HERE
		keyboard --vckeymap=us --xlayouts='us'
		lang en_US.UTF-8
		firewall --disabled
		network --bootproto=dhcp --activate
		authselect --enableshadow --passalgo=sha512
		skipx
		services --enabled="chronyd"
		bootloader --append="crashkernel=auto" --location=mbr --boot-drive=vda
		autopart --type=plain --nohome
		zerombr
		clearpart --all --initlabel --drives=vda
		timezone America/Los_Angeles --isUtc --nontp
		rootpw --plaintext  #EDIT HERE
		%packages
		@core
		chrony
		kexec-tools
		nfs-utils
		%end
		%post --log=/root/ks-postinstall.log
		mkdir -m700/root/.ssh
		curl http://192.168.95.1/id_rsa.pub -o /root/.ssh/authorized_keys
		chmod 600 /root/.ssh/authorized_keys
		%end
		%addon com_redhat_kdump --enable --reserve-mb='auto'
		%end
		%anaconda
		pwpolicy root --minlen=6 --minquality=1 --notstrict --nochanges --notempty
		pwpolicy user --minlen=6 --minquality=1 --notstrict --nochanges --notempty
		pwpolicy luks --minlen=6 --minquality=1 --notstrict --nochanges --notempty
		%end
		

  

Make sure you are still in the same directory, and enter the following:

	wget http://mirrors.ocf.berkeley.edu/almalinux/8.8/isos/x86_64/AlmaLinux-8-latest-x86_64-minimal.iso

Install the Virtual Machine:

 virt-install --name **alma8** --ram **2048** --vcpus=**2** --os-variant=almalinux8 --location=/var/lib/libvirt/boot/AlmaLinux-8-latest-x86\_64-minimal.iso --nographics --disk path=/var/lib/libvirt/images/**alma8**.qcow2,size=8,bus=virtio,format=qcow2 --network "bridge=br1,mac=**52:54:00:00:95:77**" --initrd-inject=/var/lib/libvirt/boot/alma8.ks --extra-args="console=ttyS0,115200n8 inst.ks=file://alma8.ks

  

Update the bolded areas to match your desires.
