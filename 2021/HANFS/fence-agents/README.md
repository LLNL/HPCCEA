# LLNL Powerman Fence
This is based off of a fork created by Mike Gilbert found here: [Powerman fencing agent](https://github.com/mkgilbert/fence-agents/tree/feature-powerman)
That fork contains an outdated powerman python script so I got the updated version from here:  [Powerman python script](https://github.com/ofaaland/fence-agents-powerman)
The original repo for the fencing agents can be found here: [ClusterLabs fence agents](https://github.com/ClusterLabs/fence-agents)

# Building
It is important that the fencing agent and all dependencies get installed onto *every* node in the pacemaker cluster. 

Base dependencies 
* fence-agents-common
* libwsman1
* openwsman-python3

Go in the clone folder and run:
* ./autogen.sh
* ./configure
* make && make install

## Notes
### CentOS8 Compatibility 
The make file is a little outdated with its python binary path. I resolved this temporarily by running the following before running `make && make install`
`ln -s /usr/bin/python3 /usr/bin/python`
Then I removed the symlink after the fence agent gets properlly installed 
`rm /usr/bin/python`

### Python Modules
When running `./configure` it might fail if you don't have the appropiate python modules. Depending on your setup, the missing modules might be different but they are usually just python modules. For example, I was missing a suds module so I did _dnf search python suds_ to find the correct module.

Fence agents
============
Fence agents were developed as device "drivers" which are able to prevent computers from destroying data on shared storage. Their aim is to isolate a corrupted computer, using one of three methods:

  * Power - A computer that is switched off cannot corrupt data, but it is important to not do a "soft-reboot" as we won't know if this is possible. This also works for virtual machines when the fence device is a hypervisor.
  * Network - Switches can prevent routing to a given computer, so even if a computer is powered on it won't be able to harm the data.
  * Configuration - Fibre-channel switches or SCSI devices allow us to limit who can write to managed disks.

Fence agents do not use configuration files, as configuration management is outside of their scope. All of the configuration has to be specified either as command-line arguments or lines of standard input (see the complete list for more info).

Because many fence agents are quite similar to each other, a fencing library (in Python) was developed. Please use it for further development. Creating or modifying a new fence agent should be quite simple using this library.

Detailed user and developer documentation can be found here: [https://fedorahosted.org/cluster/wiki/fence-agents](https://fedorahosted.org/cluster/wiki/fence-agents)
