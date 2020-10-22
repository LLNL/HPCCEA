#!/bin/bash

#Start xinetd
systemctl start xinetd

#update /xinetd.d/tftp
sed -i 's+/var/lib/tftpboot+/tftpboot+' /etc/xinetd.d/tftp
sed -i '/disable/ s/yes/no/' /etc/xinetd.d/tftp

#disable firwall
systemctl stop firewalld

#SElinux security fix
restorecon -Rv /tftpboot

#FTP fix
chcon -R -t public_content_t /tftpboot

#restart tftp, xinetd, and vsftpd
systemctl restart tftp xinetd vsftpd
