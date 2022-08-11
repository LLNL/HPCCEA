{\rtf1\ansi\ansicpg1252\cocoartf2638
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 ArialMT;\f1\froman\fcharset0 Times-Roman;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs29\fsmilli14667 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 ## Introduction
\f1\fs24 \

\f0\fs29\fsmilli14667 >Large computer centers must have a method of managing and effectively scheduling their resources for use. [Flux](http://flux-framework.org/) offers a framework that enables resource types and schedulers to be used. Flux makes smarter placement decisions by offering greater flexibility and adaptation.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## System Requirements
\f1\fs24 \

\f0\fs29\fsmilli14667 Three Alma 8 VMs - One VM will act as the management node and the other two VMs will act as the compute node.\'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Passwordless SSH - Ensure that you can SSH silently into the other nodes
\f1\fs24 \
\

\f0\fs29\fsmilli14667 MUNGE - Used to sign job requests submitted to Flux. Set this up if you haven't already done so.\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Creating users
\f1\fs24 \

\f0\fs29\fsmilli14667 > Create two users: flux and a standard user. Flux user will be the one who generates the key to enhance security. The standard user will run the flux jobs.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 `useradd flux`
\f1\fs24 \

\f0\fs29\fsmilli14667 `useradd christine`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Ensure that the UID and GUID are the same across all clusters. The third column is the UID. The fourth column is the GUID.
\f1\fs24 \

\f0\fs29\fsmilli14667 `cat /etc/passwd | grep flux`
\f1\fs24 \

\f0\fs29\fsmilli14667 `cat /etc/passwd | grep christine`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Setting up NFS Mount
\f1\fs24 \

\f0\fs29\fsmilli14667 > First set up NFS mount. This will make things a lot easier in the future. Mount the directories from the management node to the rest of the nodes with NFS.\'a0 The configuration files will only have to be edited once, and we will not have to make copies to the rest of the nodes.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 On the management node,
\f1\fs24 \
\

\f0\fs29\fsmilli14667 1.\'a0 Edit the /etc/exports file and add the following line\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 ```\'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 /usr/local\'a0 192.168.95.0/255.255.255.0(rw,sync,no_root_squash)
\f1\fs24 \

\f0\fs29\fsmilli14667 /home 192.168.95.0/255.255.255.0(rw,sync,no_root_squash)
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \
\

\f0\fs29\fsmilli14667 2. Restart the nfs-server with the following command
\f1\fs24 \
\

\f0\fs29\fsmilli14667 	`systemctl restart nfs-server`
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 On all compute nodes,
\f1\fs24 \
\

\f0\fs29\fsmilli14667 1.\'a0 Edit /etc/fstab and add the following line (**change to management node**):
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 esilicon1:/usr/local\'a0 /usr/local\'a0 nfs\'a0 defaults\'a0 0 0
\f1\fs24 \

\f0\fs29\fsmilli14667 esilicon1:/home /home nfs\'a0 defaults\'a0 0 0
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 2.\'a0 Mount the directory
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 	`mount /usr/local`	
\f1\fs24 \

\f0\fs29\fsmilli14667 	`mount /home`
\f1\fs24 \
\
\

\f0\fs29\fsmilli14667 ## Installation of packages
\f1\fs24 \

\f0\fs29\fsmilli14667 >Three software packages ([flux-core](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/index.html), [flux-security](https://flux-framework.readthedocs.io/projects/flux-security/en/latest/index.html), [flux-sched](https://github.com/flux-framework/flux-sched)) must be installed before using flux.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Install epel release
\f1\fs24 \

\f0\fs29\fsmilli14667 `dnf install -y epel-release`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Enable epel repo and powertools repo on all nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `dnf config-manager --enable epel`
\f1\fs24 \

\f0\fs29\fsmilli14667 `dnf config-manager --set-enabled powertools`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Install Alma 8 packages on all nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `dnf install -y autoconf automake libtool make pkgconfig glibc-devel zeromq-devel czmq-devel libuuid-devel jansson-devel lz4-devel libarchive-devel hwloc-devel sqlite-devel lua lua-devel lua-posix python3-devel python3-cffi python3-yaml python3-jsonschema python3-sphinx aspell aspell-en valgrind-devel mpich-devel jq libsodium-devel jansson-devel libuuid-devel munge-devel hwloc-devel boost-devel boost-graph boost-system boost-filesystem boost-regex libedit-devel libxml2-devel python3-pyyaml yaml-cpp-devel gcc-c++`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Do the following on the management node. Make sure to install flux-security first then flux-core. flux-core builds on flux-security which is what allows flux to run as multi-users.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Install flux-security
\f1\fs24 \

\f0\fs29\fsmilli14667 1. `cd`
\f1\fs24 \

\f0\fs29\fsmilli14667 2.`git clone https://github.com/flux-framework/flux-security`
\f1\fs24 \

\f0\fs29\fsmilli14667 3. `cd flux-security`
\f1\fs24 \

\f0\fs29\fsmilli14667 4. `./autogen.sh`
\f1\fs24 \

\f0\fs29\fsmilli14667 5. `./configure`
\f1\fs24 \

\f0\fs29\fsmilli14667 6. `make` # Looks into makefile directory and recompiles the files
\f1\fs24 \

\f0\fs29\fsmilli14667 7. `make install` # Installs into /usr/local/bin
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Install flux-core
\f1\fs24 \

\f0\fs29\fsmilli14667 1. `cd`
\f1\fs24 \

\f0\fs29\fsmilli14667 2. `git clone https://github.com/flux-framework/flux-core.git`
\f1\fs24 \

\f0\fs29\fsmilli14667 3.\'a0 `cd flux-core`
\f1\fs24 \

\f0\fs29\fsmilli14667 4. `./autogen.sh`
\f1\fs24 \

\f0\fs29\fsmilli14667 5. `PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure --with-flux-security` # Allow flux jobs to run as user other than flux
\f1\fs24 \

\f0\fs29\fsmilli14667 6. `make`\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 7. `make install`\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Install flux-sched
\f1\fs24 \

\f0\fs29\fsmilli14667 1. `cd`
\f1\fs24 \

\f0\fs29\fsmilli14667 2. `git clone https://github.com/flux-framework/flux-sched.git`
\f1\fs24 \

\f0\fs29\fsmilli14667 3. `cd flux-sched`
\f1\fs24 \

\f0\fs29\fsmilli14667 4. `./autogen.sh`
\f1\fs24 \

\f0\fs29\fsmilli14667 5. `./configure`
\f1\fs24 \

\f0\fs29\fsmilli14667 6. `make`\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 7. `make install`\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Configuring flux-security\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 >Job requests are signed using a library provided by flux-security. This ensures authenticity. This library reads configuration from /usr/local/etc/flux/security/conf.d/*.toml.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 View the following file:
\f1\fs24 \

\f0\fs29\fsmilli14667 `cat /usr/local/etc/flux/security/conf.d/sign.toml`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Ensure it looks like the content below:
\f1\fs24 \

\f0\fs29\fsmilli14667 ```\'a0\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 # Job requests should be valid for 2 weeks\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 # Use munge as the job request signing mechanism\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 [sign]\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 max-ttl = 1209600\'a0 # 2 weeks\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 default-type = "munge"\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 allowed-types = [ "munge" ]
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Configuring the IMP
\f1\fs24 \

\f0\fs29\fsmilli14667 >IMP (Independent Minister of Privileges) allows instance owners to run work on behalf of a guest. It has a private configuration space in /usr/local/etc/flux/imp/conf.d/*.toml
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Make the following directory
\f1\fs24 \

\f0\fs29\fsmilli14667 `mkdir -p /usr/local/etc/flux/imp/conf.d`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Edit imp.toml
\f1\fs24 \

\f0\fs29\fsmilli14667 `vi /usr/local/etc/flux/imp/conf.d/imp.toml`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Adding the following lines:
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 # Only allow access to the IMP exec method by the 'flux' user.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Only allow the installed version of flux-shell(1) to be executed.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [exec]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 allowed-users = [ "flux" ]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 allowed-shells = [ "/usr/local/libexec/flux/flux-shell" ]
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Change permissions of the file. This is so that flux jobs can be ran under a standard user.
\f1\fs24 \

\f0\fs29\fsmilli14667 `chmod 4755 /usr/local/libexec/flux/flux-imp`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Configuring the Network Certificate
\f1\fs24 \

\f0\fs29\fsmilli14667 >Overlay network security requires a certificate to be distributed to all nodes and should only be readable by the flux user.
\f1\fs24 \
\
\

\f0\fs29\fsmilli14667 Log in as flux user:
\f1\fs24 \

\f0\fs29\fsmilli14667 `sudo su - flux`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Generate key:
\f1\fs24 \

\f0\fs29\fsmilli14667 `flux keygen /tmp/curve.cert`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Log out of flux:
\f1\fs24 \

\f0\fs29\fsmilli14667 `exit`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Make directory:
\f1\fs24 \

\f0\fs29\fsmilli14667 `mkdir -p /usr/local/etc/flux/system/`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Move the key:
\f1\fs24 \

\f0\fs29\fsmilli14667 `mv /tmp/curve.cert /usr/local/etc/flux/system/`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Since we have /usr/local mounted, the certificate will also be copied over to the other nodes automatically.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Configuring the Flux System Instance
\f1\fs24 \

\f0\fs29\fsmilli14667 Make directory:
\f1\fs24 \

\f0\fs29\fsmilli14667 `mkdir -p /usr/local/etc/flux/system/conf.d`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Edit system.toml file:\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 `vi /usr/local/etc/flux/system/conf.d/system.toml`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Make it same as the contents below. **==Change hosts to correct cluster.==**
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 # Flux needs to know the path to the IMP executable
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [exec]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 imp = "/usr/local/libexec/flux/flux-imp"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Allow users other than the instance owner (guests) to connect to Flux
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Optionally, root may be given "owner privileges" for convenience
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [access]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 allow-guest-user = true
\f1\fs24 \
\

\f0\fs29\fsmilli14667 allow-root-owner = true
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Point to shared network certificate generated flux-keygen(1).
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Define the network endpoints for Flux's tree based overlay network
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # and inform Flux of the hostnames that will start flux-broker(1).
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [bootstrap]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 curve_cert = "/usr/local/etc/flux/system/curve.cert"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 default_port = 8050
\f1\fs24 \
\

\f0\fs29\fsmilli14667 default_bind = "tcp://*:%p"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 default_connect = "tcp://%h:%p"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 hosts = [
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \{ host = "siliconi,silicon[2-5]" \},
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Speed up detection of crashed network peers (system default is around 20m)
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [tbon]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 tcp_user_timeout = "2m"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Point to resource definition generated with flux-R(1).
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Uncomment to exclude nodes (e.g. mgmt, login), from eligibility to run jobs.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [resource]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 path = "/usr/local/etc/flux/system/R"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 #exclude = "test[1-2]"
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 # Remove inactive jobs from the KVS after one week.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 [job-manager]
\f1\fs24 \
\

\f0\fs29\fsmilli14667 inactive-age-limit = "7d"
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 > Note: Default bind must be *:%p because the management node and compute nodes have different physical adapters.\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 ## Configuring Resources
\f1\fs24 \

\f0\fs29\fsmilli14667 >`flux R encode` encodes the arguments into RFC 20 (ASCII format for network interchange). You can assign string-based properties to ranks using the properties field in R. Properties are used in job constraints specified by users on the command line. At the minimum, a hostlist and core idset must be specified
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Generate RFC 20 format (**Change to correct cluster under hosts**):
\f1\fs24 \

\f0\fs29\fsmilli14667 `flux R encode --hosts=siliconi,silicon[2-5] --cores=0-3 >/usr/local/etc/flux/system/R`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 View the RFC 20 generated format:
\f1\fs24 \

\f0\fs29\fsmilli14667 `cat /usr/local/etc/flux/system/R`
\f1\fs24 \

\f0\fs29\fsmilli14667 ![](https://i.imgur.com/vx4vuAO.png)
\f1\fs24 \
\
\

\f0\fs29\fsmilli14667 ## Getting Flux to start on boot up
\f1\fs24 \

\f0\fs29\fsmilli14667 >Flux.service file needs to be copied to system default location so that flux can be started, stopped, enabled, and disabled with systemctl.
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Copy the flux.service file into the system default location on all nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `cp /usr/local/usr/lib/systemd/system/flux.service /usr/lib/systemd/system/`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Enable and start flux on all nodes.
\f1\fs24 \

\f0\fs29\fsmilli14667 `systemctl enable --now flux`\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Check that flux is running on all nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `systemctl status flux`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Display free nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `flux resource list`
\f1\fs24 \

\f0\fs29\fsmilli14667 ![](https://i.imgur.com/pJ1PuP0.png)
\f1\fs24 \
\
\

\f0\fs29\fsmilli14667 ## Running a job
\f1\fs24 \

\f0\fs29\fsmilli14667 >[flux mini run](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-mini.html) submits jobs to run under Flux.\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 -n: Sets the number of tasks to launch. Default is 1.
\f1\fs24 \

\f0\fs29\fsmilli14667 -N: Sets the number of nodes to assign to the job. If unspecified, the number of nodes will be chosen by the scheduler.\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 >Tasks will be distributed across the nodes. **Number of nodes cannot be greater than number of tasks**.\'a0
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Log in as standard user
\f1\fs24 \

\f0\fs29\fsmilli14667 `sudo su - christine`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Submit a job with two tasks and two nodes:
\f1\fs24 \

\f0\fs29\fsmilli14667 `flux mini run -n2 -N2 hostname 2>/dev/null | grep -v cpu-affinity`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Example outputs:
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 [christine@nvm2 ~]$ flux mini run -n2 -N2 hostname 2>/dev/null | grep -v cpu-affinity\'a0
\f1\fs24 \

\f0\fs29\fsmilli14667 nvm3 nvm4
\f1\fs24 \

\f0\fs29\fsmilli14667 [christine@nvm2 ~]$ flux mini run -n2 -N1 hostname 2>/dev/null | grep -v cpu-affinity
\f1\fs24 \

\f0\fs29\fsmilli14667 nvm4 nvm4
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 ## Running an MPI job
\f1\fs24 \

\f0\fs29\fsmilli14667 Install mpicc if you haven't already done so:
\f1\fs24 \

\f0\fs29\fsmilli14667 `dnf install -y openmpi-devel`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Create a file called hello.c
\f1\fs24 \

\f0\fs29\fsmilli14667 `vi hello.c`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Add the following contents
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 #include <mpi.h>
\f1\fs24 \

\f0\fs29\fsmilli14667 #include <stdio.h>
\f1\fs24 \
\

\f0\fs29\fsmilli14667 int main(int argc, char** argv) \{
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Initialize the MPI environment
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0MPI_Init(NULL, NULL);
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Get the number of processes
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0int world_size;
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0MPI_Comm_size(MPI_COMM_WORLD, &world_size);
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Get the rank of the process
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0int world_rank;
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Get the name of the processor
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0char processor_name[MPI_MAX_PROCESSOR_NAME];
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0int name_len;
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0MPI_Get_processor_name(processor_name, &name_len);
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Print off a hello world message
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0printf("Hello world from processor %s, rank %d"
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0" out of %d processors\\n",
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0\'a0processor_name, world_rank, world_size);
\f1\fs24 \
\

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0// Finalize the MPI environment.
\f1\fs24 \

\f0\fs29\fsmilli14667 \'a0\'a0\'a0\'a0MPI_Finalize();
\f1\fs24 \

\f0\fs29\fsmilli14667 \}
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 Compile the file:
\f1\fs24 \

\f0\fs29\fsmilli14667 `/usr/lib64/openmpi/bin/mpicc -o hello hello.c`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Submit the job (Change to correct directory)
\f1\fs24 \

\f0\fs29\fsmilli14667 ` flux mini run -n2 -N2 /home/christine/hello 2>/dev/null | grep -v cpu-affinity`
\f1\fs24 \
\

\f0\fs29\fsmilli14667 Expected output:
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \

\f0\fs29\fsmilli14667 [christine@nvm2 ~]$ flux mini run -n2 -N2 /home/christine/hello 2>/dev/null | grep -v cpu-affinity
\f1\fs24 \

\f0\fs29\fsmilli14667 Hello world from processor nvm3, rank 0 out of 2 processors
\f1\fs24 \

\f0\fs29\fsmilli14667 Hello world from processor nvm4, rank 1 out of 2 processors
\f1\fs24 \

\f0\fs29\fsmilli14667 ```
\f1\fs24 \
\
\
\
}