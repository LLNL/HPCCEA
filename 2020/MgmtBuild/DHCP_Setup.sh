#!/usr/bin/bash

a=$1

dfile=/etc/dhcp/dhcpd.conf

input="/etc/hostname"
while IFS= read -r line
do
	if [ "$line" != "localhost.localdomain" ]; then
		HOSTNAME="$line"
	fi
done < "$input"

n=${HOSTNAME::${#HOSTNAME}-1}


cat << HERE > $dfile
option space pxelinux;
option pxelinux.magic      code 208 = string;
option pxelinux.configfile code 209 = text;
option pxelinux.pathprefix code 210 = text;
option pxelinux.reboottime code 211 = unsigned integer 32;
not authoritative;
use-host-decl-names true;
 
site-option-space "pxelinux";
option pxelinux.magic f1:00:74:7e;
if exists dhcp-parameter-request-list {
        option dhcp-parameter-request-list = concat(option
dhcp-parameter-request-list,d0,d1,d2,d3);
}
 
option pxelinux.reboottime 30;
max-lease-time -1;
default-lease-time -1;
 
##### change this subnet to match your setup ####
subnet ${a}0 netmask 255.255.255.0 {
    option routers ${a}1;
    option domain-name "llnl.gov";
    option domain-name-servers 192.12.17.17;
    option subnet-mask 255.255.255.0;
    option broadcast-address ${a}255; 
 
    use-host-decl-names on;
    option vendor-encapsulated-options 3c:09:45:74:68:65:72:62:6f:6f:74:ff;
    option root-path        "/tftpboot";
    group {
	next-server  ${a}1;  # CHANGE THIS
HERE

#for node in {2..5}
input="macAddr.txt"
ctr=2
while IFS= read -r line
do
        macnode=$line
	cat << HERE >> $dfile
	    host ${n}$ctr {
            	hardware ethernet $macnode;
            	fixed-address ${a}$ctr;  # CHANGE THIS
            	option host-name "${n}$ctr";  # CHANGE THIS
            	filename "/pxelinux.0";
	    }
HERE
	ctr=$((ctr+1));
done < "$input"	

cat << HERE >> $dfile
	}
}
HERE

systemctl enable dhcpd
systemctl start dhcpd
