#!/bin/bash

# Arguments
# $1 = cluster
# $2 = IP of mgmt node public interface
# $3 = base IP for mgmt net
# $4 = base IP for IB net
# $5 = base IP for IPMI net

OUTFILE=/etc/hosts

CLUSTERNAME=$1 # xenon

MGMTPUBIP=$2 # 192.168.59. 

BASEMGMTIP=$3 # 192.168.95.

BASEIBIP=$4   #192.168.123.

BASEMIPMIIP=$5 #192.168.96.

#Local hosts
echo 127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4 > $OUTFILE
echo ::1         ipv6-localhost >> $OUTFILE

# put in mgmt pub IP
echo $MGMTPUBIP   ${CLUSTERNAME}i >> $OUTFILE

# create /etc/hostname
echo ${CLUSTERNAME}i > /etc/hostname

# Management IPs
# mgmt node is first IP on mgmt net and has additional alias
echo ${BASEMGMTIP}1  e${CLUSTERNAME}1 e1 e${CLUSTERNAME}i  >> $OUTFILE
for node in {2..5}
do
   echo ${BASEMGMTIP}$node  e${CLUSTERNAME}$node e$node >> $OUTFILE
done
  

#IB IPs - BASEIBIP=$4  
#mgmt node is first IP on IB and has additional alias
echo ${BASEIBIP}1  h${CLUSTERNAME}i h${CLUSTERNAME}1 h1 ${CLUSTERNAME}1 >> $OUTFILE
for node in {2..5}
do
   echo ${BASEIBIP}$node  h${CLUSTERNAME}$node h$node ${CLUSTERNAME}$node >> $OUTFILE
done

# MIP IPS - BASEMIPMIIP=$5
#mgmt node is first IP on IB and has additional alias
echo ${BASEMIPMIIP}1  p${CLUSTERNAME}i p${CLUSTERNAME}1  p1 >> $OUTFILE
for node in {2..5}
do 
   echo ${BASEMIPMIIP}$node p${CLUSTERNAME}$node p$node >> $OUTFILE
done
