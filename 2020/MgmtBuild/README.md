Scripts to customize a managemenet node that had just been installed with CentOS 7

File "macAddr.txt" should be populated with the MAC addrs of client nodes before running build.sh

Run the build.sh script with arguments like below (args are described in build.sh)

bash ./build.sh clustername  192.168.59.3  192.168.95.  192.168.124.  192.168.96. ROOTPASSWORD

Note alot of assumptions are made about the system, for example netmasks on interfaces, etc.

