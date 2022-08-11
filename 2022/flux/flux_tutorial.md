## Introduction
>Large computer centers must have a method of managing and effectively scheduling their resources for use. [Flux](http://flux-framework.org/) offers a framework that enables resource types and schedulers to be used. Flux makes smarter placement decisions by offering greater flexibility and adaptation.

## System Requirements
Three Alma 8 VMs - One VM will act as the management node and the other two VMs will act as the compute node.  

Passwordless SSH - Ensure that you can SSH silently into the other nodes

MUNGE - Used to sign job requests submitted to Flux. Set this up if you haven't already done so. 

## Creating users
> Create two users: flux and a standard user. Flux user will be the one who generates the key to enhance security. The standard user will run the flux jobs.

`useradd flux`
`useradd christine`

Ensure that the UID and GUID are the same across all clusters. The third column is the UID. The fourth column is the GUID.
`cat /etc/passwd | grep flux`
`cat /etc/passwd | grep christine`

## Setting up NFS Mount
> First set up NFS mount. This will make things a lot easier in the future. Mount the directories from the management node to the rest of the nodes with NFS.  The configuration files will only have to be edited once, and we will not have to make copies to the rest of the nodes.

  
On the management node,

1.  Edit the /etc/exports file and add the following line 
```    
/usr/local  192.168.95.0/255.255.255.0(rw,sync,no_root_squash)
/home 192.168.95.0/255.255.255.0(rw,sync,no_root_squash)
```

2. Restart the nfs-server with the following command

	`systemctl restart nfs-server`
    
    
On all compute nodes,

1.  Edit /etc/fstab and add the following line (**change to management node**):
```
esilicon1:/usr/local  /usr/local  nfs  defaults  0 0
esilicon1:/home /home nfs  defaults  0 0
```
    

2.  Mount the directory
    
	`mount /usr/local`	
	`mount /home`


## Installation of packages
>Three software packages ([flux-core](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/index.html), [flux-security](https://flux-framework.readthedocs.io/projects/flux-security/en/latest/index.html), [flux-sched](https://github.com/flux-framework/flux-sched)) must be installed before using flux.

Install epel release
`dnf install -y epel-release`

Enable epel repo and powertools repo on all nodes:
`dnf config-manager --enable epel`
`dnf config-manager --set-enabled powertools`

Install Alma 8 packages on all nodes:
`dnf install -y autoconf automake libtool make pkgconfig glibc-devel zeromq-devel czmq-devel libuuid-devel jansson-devel lz4-devel libarchive-devel hwloc-devel sqlite-devel lua lua-devel lua-posix python3-devel python3-cffi python3-yaml python3-jsonschema python3-sphinx aspell aspell-en valgrind-devel mpich-devel jq libsodium-devel jansson-devel libuuid-devel munge-devel hwloc-devel boost-devel boost-graph boost-system boost-filesystem boost-regex libedit-devel libxml2-devel python3-pyyaml yaml-cpp-devel gcc-c++`

Do the following on the management node. Make sure to install flux-security first then flux-core. flux-core builds on flux-security which is what allows flux to run as multi-users.

Install flux-security
1. `cd`
2.`git clone https://github.com/flux-framework/flux-security`
3. `cd flux-security`
4. `./autogen.sh`
5. `./configure`
6. `make` # Looks into makefile directory and recompiles the files
7. `make install` # Installs into /usr/local/bin

Install flux-core
1. `cd`
2. `git clone https://github.com/flux-framework/flux-core.git`
3.  `cd flux-core`
4. `./autogen.sh`
5. `PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure --with-flux-security` # Allow flux jobs to run as user other than flux
6. `make` 
7. `make install` 

Install flux-sched
1. `cd`
2. `git clone https://github.com/flux-framework/flux-sched.git`
3. `cd flux-sched`
4. `./autogen.sh`
5. `./configure`
6. `make` 
7. `make install` 

## Configuring flux-security 
>Job requests are signed using a library provided by flux-security. This ensures authenticity. This library reads configuration from /usr/local/etc/flux/security/conf.d/*.toml.

View the following file:
`cat /usr/local/etc/flux/security/conf.d/sign.toml`

Ensure it looks like the content below:
```  
# Job requests should be valid for 2 weeks 
# Use munge as the job request signing mechanism 
[sign] 
max-ttl = 1209600  # 2 weeks 
default-type = "munge" 
allowed-types = [ "munge" ]
```

## Configuring the IMP
>IMP (Independent Minister of Privileges) allows instance owners to run work on behalf of a guest. It has a private configuration space in /usr/local/etc/flux/imp/conf.d/*.toml

Make the following directory
`mkdir -p /usr/local/etc/flux/imp/conf.d`

Edit imp.toml
`vi /usr/local/etc/flux/imp/conf.d/imp.toml`

Adding the following lines:
```
# Only allow access to the IMP exec method by the 'flux' user.

# Only allow the installed version of flux-shell(1) to be executed.

[exec]

allowed-users = [ "flux" ]

allowed-shells = [ "/usr/local/libexec/flux/flux-shell" ]
```

Change permissions of the file. This is so that flux jobs can be ran under a standard user.
`chmod 4755 /usr/local/libexec/flux/flux-imp`

## Configuring the Network Certificate
>Overlay network security requires a certificate to be distributed to all nodes and should only be readable by the flux user.


Log in as flux user:
`sudo su - flux`

Generate key:
`flux keygen /tmp/curve.cert`

Log out of flux:
`exit`

Make directory:
`mkdir -p /usr/local/etc/flux/system/`

Move the key:
`mv /tmp/curve.cert /usr/local/etc/flux/system/`

Since we have /usr/local mounted, the certificate will also be copied over to the other nodes automatically.

## Configuring the Flux System Instance
Make directory:
`mkdir -p /usr/local/etc/flux/system/conf.d`

Edit system.toml file: 
`vi /usr/local/etc/flux/system/conf.d/system.toml`

Make it same as the contents below. **==Change hosts to correct cluster.==**
```
# Flux needs to know the path to the IMP executable

[exec]

imp = "/usr/local/libexec/flux/flux-imp"

  

# Allow users other than the instance owner (guests) to connect to Flux

# Optionally, root may be given "owner privileges" for convenience

[access]

allow-guest-user = true

allow-root-owner = true

  

# Point to shared network certificate generated flux-keygen(1).

# Define the network endpoints for Flux's tree based overlay network

# and inform Flux of the hostnames that will start flux-broker(1).

[bootstrap]

curve_cert = "/usr/local/etc/flux/system/curve.cert"

  

default_port = 8050

default_bind = "tcp://*:%p"

default_connect = "tcp://%h:%p"

  

hosts = [

{ host = "siliconi,silicon[2-5]" },

]

  

# Speed up detection of crashed network peers (system default is around 20m)

[tbon]

tcp_user_timeout = "2m"

  

# Point to resource definition generated with flux-R(1).

# Uncomment to exclude nodes (e.g. mgmt, login), from eligibility to run jobs.

[resource]

path = "/usr/local/etc/flux/system/R"

#exclude = "test[1-2]"

  

# Remove inactive jobs from the KVS after one week.

[job-manager]

inactive-age-limit = "7d"
```
> Note: Default bind must be *:%p because the management node and compute nodes have different physical adapters. 

## Configuring Resources
>`flux R encode` encodes the arguments into RFC 20 (ASCII format for network interchange). You can assign string-based properties to ranks using the properties field in R. Properties are used in job constraints specified by users on the command line. At the minimum, a hostlist and core idset must be specified

Generate RFC 20 format (**Change to correct cluster under hosts**):
`flux R encode --hosts=siliconi,silicon[2-5] --cores=0-3 >/usr/local/etc/flux/system/R`

View the RFC 20 generated format:
`cat /usr/local/etc/flux/system/R`
![](https://i.imgur.com/vx4vuAO.png)


## Getting Flux to start on boot up
>Flux.service file needs to be copied to system default location so that flux can be started, stopped, enabled, and disabled with systemctl.

Copy the flux.service file into the system default location on all nodes:
`cp /usr/local/usr/lib/systemd/system/flux.service /usr/lib/systemd/system/`

Enable and start flux on all nodes.
`systemctl enable --now flux` 

Check that flux is running on all nodes:
`systemctl status flux`

Display free nodes:
`flux resource list`
![](https://i.imgur.com/pJ1PuP0.png)


## Running a job
>[flux mini run](https://flux-framework.readthedocs.io/projects/flux-core/en/latest/man1/flux-mini.html) submits jobs to run under Flux. 
-n: Sets the number of tasks to launch. Default is 1.
-N: Sets the number of nodes to assign to the job. If unspecified, the number of nodes will be chosen by the scheduler. 

>Tasks will be distributed across the nodes. **Number of nodes cannot be greater than number of tasks**. 

Log in as standard user
`sudo su - christine`

Submit a job with two tasks and two nodes:
`flux mini run -n2 -N2 hostname 2>/dev/null | grep -v cpu-affinity`

Example outputs:
```
[christine@nvm2 ~]$ flux mini run -n2 -N2 hostname 2>/dev/null | grep -v cpu-affinity 
nvm3 nvm4
[christine@nvm2 ~]$ flux mini run -n2 -N1 hostname 2>/dev/null | grep -v cpu-affinity
nvm4 nvm4
```
## Running an MPI job
Install mpicc if you haven't already done so:
`dnf install -y openmpi-devel`

Create a file called hello.c
`vi hello.c`

Add the following contents
```
#include <mpi.h>
#include <stdio.h>

int main(int argc, char** argv) {
    // Initialize the MPI environment
    MPI_Init(NULL, NULL);

    // Get the number of processes
    int world_size;
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    // Get the rank of the process
    int world_rank;
    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);

    // Get the name of the processor
    char processor_name[MPI_MAX_PROCESSOR_NAME];
    int name_len;
    MPI_Get_processor_name(processor_name, &name_len);

    // Print off a hello world message
    printf("Hello world from processor %s, rank %d"
           " out of %d processors\n",
           processor_name, world_rank, world_size);

    // Finalize the MPI environment.
    MPI_Finalize();
}
```
Compile the file:
`/usr/lib64/openmpi/bin/mpicc -o hello hello.c`

Submit the job (Change to correct directory)
` flux mini run -n2 -N2 /home/christine/hello 2>/dev/null | grep -v cpu-affinity`

Expected output:
```
[christine@nvm2 ~]$ flux mini run -n2 -N2 /home/christine/hello 2>/dev/null | grep -v cpu-affinity
Hello world from processor nvm3, rank 0 out of 2 processors
Hello world from processor nvm4, rank 1 out of 2 processors
```




