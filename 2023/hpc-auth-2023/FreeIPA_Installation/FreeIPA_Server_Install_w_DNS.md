<a name="br1"></a> 

**FreeIPA Server + DNS Install**

**References**

[Server installation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/installing_identity_management/installing-an-ipa-server-without-a-ca_installing-identity-management)

[Client installation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/html/installing_identity_management/assembly_installing-an-idm-client_installing-identity-management#installing-ipa-client-non-interactive-install_assembly_installing-an-idm-client)

[Removing host entries](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/identity_management_guide/host-disable#host-disable-proc)

**Do not use mgmt node**

Use a compute node or a VM (it will be slower), and NOT the management node

1. Create a CentOS or Alma8 VM on a compute node 
2. Disable firewall

**Free-IPA Server Installation on Compute Node (do this as root)**

1. Install and enable some dependencies.

```
dnf install epel-release

dnf module enable idm:DL1
```

2. Disable firewalld. This will open necessary ports for FreeIPA to run through.
```
systemctl stop firewalld

systemctl disable firewalld
```
3. Configure your /etc/hosts and /etc/hostname IN THE COMPUTE NODE slightly differently. You're going to need a fully qualified domain name (FQDN), in order for DNS to work.
```
# vi into /etc/hosts add the following line to the ip address of your node. Make sure the FQDN is listed first

192.168.95.x eclusterX.ipa.test eclusterX ex

# this command will change your hostname. You can also just vi into /etc/hostname and change directly

hostnamectl set-hostname {eclusterX}.ipa.test --static
```
After editing those files, reboot the node and it should save those changes. When you re-enter the node, check your hostname like this:
```
[root@clusterx ~]# hostname

eclusterx.ipa.test
```

**Install FreeIPA server + DNS server**

1. Install freeipa server and DNS packages

``# dnf install freeipa-server freeipa-server-dns``

2. Configure freeipa server + DNS server

``# ipa-server-install``

The log file for this installation can be found in /var/log/ipaserver-install.log

    ==============================================================================

    This program will set up the IPA Server.

    Version 4.9.11

    This includes:

        * Configure a stand-alone CA (dogtag) for certificate management

        * Configure the NTP client (chronyd)

        * Create and configure an instance of Directory Server

        * Create and configure a Kerberos Key Distribution Center (KDC)

        * Configure Apache (httpd)

        * Configure SID generation

        * Configure the KDC to enable PKINIT

    To accept the default shown in brackets, press the Enter key.

    Do you want to configure integrated DNS (BIND)? [no]: yes

    Enter the fully qualified domain name of the computer

    on which you're setting up server software. Using the form

    <hostname>.<domainname>

    Example: master.example.com



    Server host name [eclusterx.ipa.test]:

    The domain name has been determined based on the host name.

    Please confirm the domain name [ipa.test]:

    The kerberos protocol requires a Realm name to be defined.

    This is typically the domain name converted to uppercase.

    Please provide a realm name [IPA.TEST]:

    Certain directory server operations require an administrative user.

    This user is referred to as the Directory Manager and has full access

    to the Directory for system management tasks and will be added to the

    instance of directory server created for IPA.

    The password must be at least 8 characters long.

    Directory Manager password: #enter a password of your choosing

    Password (confirm):

    The IPA server requires an administrative user, named 'admin'.

    This user is a regular system account used for IPA server administration.

    IPA admin password: #enter a password of your choosing

    Password (confirm):

    Checking DNS domain ipa.test., please wait

    ...

    Do you want to configure DNS forwarders? [yes]:

    Following DNS servers are configured in /etc/resolv.conf: 192.12.17.17

    server  # the external DNS

    Do you want to configure these servers as DNS forwarders? [yes]:

    All detected DNS servers were added. You can enter additional addresses now:

    Enter an IP address for a DNS forwarder, or press Enter to skip:

    DNS forwarders:

    192.12.17.17

    Checking DNS forwarders, please wait

    ...

    Do you want to search for missing reverse zones? [yes]:

    Checking DNS domain 95.168.192.in-addr.arpa., please wait

    ...

    Do you want to create reverse zone for IP 192.168.95.2

    [yes]:

    Please specify the reverse zone name [95.168.192.in-addr.arpa.]:

    Checking DNS domain 95.168.192.in-addr.arpa., please wait

    ...

    Using reverse zone(s) 95.168.192.in-addr.arpa.

    Trust is configured but no NetBIOS domain name found, setting it now.

    Enter the NetBIOS name for the IPA domain.

    Only up to 15 uppercase ASCII letters, digits and dashes are allowed.

    Example: EXAMPLE.



    NetBIOS domain name [IPA]:

    Do you want to configure chrony with NTP server or pool address [no]:

    The IPA Master Server will be configured with:

    Hostname: eclusterX.ipa.test

    IP address(es): 192.168.95.x

    Domain name: ipa.test

    Realm name: IPA.TEST

    

    The CA will be configured with:

    Subject DN:

    CN=Certificate Authority,O=IPA.TEST

    Subject base: O=IPA.TEST

    Chaining: self-signed

    BIND DNS server will be configured to serve IPA domain with:

    Forwarders: 192.12.17.17

    Forward policy: only

    Reverse zone(s): 95.168.192.in-addr.arpa. Continue to configure the system with these values? [no]: yes

    The following operations may take some minutes to complete.

    Please wait until the prompt is returned.

    This install took about 15 minutes. You'll know the installation was successful with the following output:

    ==============================================================================

    Setup complete

    Next steps:

    1. You must make sure these network ports are open:

    TCP Ports:

        * 80, 443: HTTP/HTTPS

        * 389, 636: LDAP/LDAPS

        * 88, 464: kerberos

        * 53: bind

    UDP Ports:

        * 88, 464: kerberos

        * 53: bind

        * 123: ntp

    2. You can now obtain a kerberos ticket using the command: 'kinit admin'

    This ticket will allow you to use the IPA tools (e.g., ipa user-add) and the web user interface.

    Be sure to back up the CA certificates stored in /root/cacert.p12

    These files are required to create replicas. The password for these

    files is the Directory Manager password

    The ipa-server-install command was successful

3. Check that you can DNS lookup the server you just created

`# dig +short eclusterX.ipa.test`

    192.168.95.x

    # nslookup eclusterX.ipa.test

    Server:

    192.168.95.x

    Address:

    192.168.95.x#53

    Name:

    eclusterX.ipa.test

    Address: 192.168.95.x

**Using the Web UI as Admin (do this as user)**

1. Download firefox, xauth, and xterm, which allows the compute node to access the local https network.

`dnf install -y firefox xauth xterm`

2. Switch to your user rather than running on root. Make sure that your administrative ticket is valid and running and type in your password.

After that, print the ticket.
```
# this will make the ticket and prompt for the password

kinit admin

# this will print the ticket

klist
```
3\. Enter a VNC Window. This will allow you to view your page. Within the VNC, ssh into lgw2-pub with your user. From there, specify the xauth permissions with the -X tag when we ssh.
```
# first, ssh into management from lgw2-pub

ssh -X user@clusteri

# check if xterm works

xterm

# close that window and ssh into the compute node that is running the ipa server

ssh -X user@ex

# check if xterm works

xterm

# if it works bring up a firefox window

firefox --no-remote
```

4. Within that firefox window type in the domain name you set up (ex. <https://eclusterx.ipa.test)>. You should be able to see your website!



**Useful "start over" commands**
```
$ ipa-server-install --uninstall # uninstall failed ipa server

$ dnf remove ipa-server          # remove ipa-server packages

$ dnf ipa-server                 # removes the ipa-server packages from the system along with any packages depending on the packages being removed
```

**Interactive FreeIPA Client Installation and Configuration**

1. Select a different compute node than the one running the IPA server. To begin, follow a similar format of installing dependencies and disabling firewalls:
```
# installing dependencies

dnf install epel-release
dnf module enable idm:DL1
dnf install -y ipa-client

# disabling firewalls

systemctl stop firewalld
systemctl disable firewalld
```

2. Change your hostname to another fully qualified hostname. (example: client.ipa.test)
```
# vi into /etc/hosts add the following line to the ip address of your node. Make sure the FQDN is listed first

192.168.95.x client.ipa.test eclusterX ex

# this command will change your hostname. You can also just vi into /etc/hostname and change directly

hostnamectl set-hostname client.ipa.test --static
```
3. Edit your /etc/resolv.conf file to point to your DNS server. This allows the NetworkManager to find your ipa-server. Since you integrated a DNS with your ipa-server, then point the nameserver to the IP of that node.
```
# vi into /etc/resolv.conf and make it look like this

nameserver 192.168.95.x
search ipa.test

# the IP address of your DNS server

# the domain of your server DNS. Should be ipa.test if you followed this tutorial example
```
Test that you can dig or nslookup your ipa-server.
```
# this command tries to find this domain name

nslookup eclusteri.ipa.test

# once it's found, it will give you information similar to this

Server: 192.168.95.1
Address:192.168.95.1#53

Name:   eclusteri.ipa.test
Address: 192.168.95.x
```
4. Next we will go through with the client configuration. Answer the prompts accordingly:
```
# ipa-client-install

This program will set up IPA client.

Version 4.9.11

Discovery was successful!

Do you want to configure chrony with NTP server or pool address? [no]:

Client hostname: client.ipa.test

Realm: IPA.TEST

DNS Domain: ipa.test

IPA Server: eclusterX.ipa.test

BaseDN: dc=ipa,dc=test

Continue to configure the system with these values? [no]: yes

Synchronizing time

No SRV records of NTP servers found and no NTP server or pool address was provided.

Using default chrony configuration.

Attempting to sync time with chronyc.

Time synchronization was successful.

User authorized to enroll computers: admin

Password for admin@IPA.TEST:

# enter server admin username

# enter the admin password you set

Successfully retrieved CA cert

Subject:

Issuer:

CN=Certificate Authority,O=IPA.TEST

CN=Certificate Authority,O=IPA.TEST

Valid From: 2023-07-26 16:20:08

Valid Until: 2043-07-26 16:20:08

Enrolled in IPA realm IPA.TEST

Created /etc/ipa/default.conf

Configured /etc/sssd/sssd.conf

Systemwide CA database updated.

Hostname (client.ipa.test) does not have A/AAAA record.

Missing reverse record(s) for address(es): 192.168.95.3.

Adding SSH public key from /etc/ssh/ssh_host_ed25519_key.pub

Adding SSH public key from /etc/ssh/ssh_host_ecdsa_key.pub

Adding SSH public key from /etc/ssh/ssh_host_rsa_key.pub

SSSD enabled

Configured /etc/openldap/ldap.conf

Configured /etc/ssh/ssh_config

Configured /etc/ssh/sshd_config

Configuring ipa.test as NIS domain.

Configured /etc/krb5.conf for IPA realm IPA.TEST

Client configuration complete.

The ipa-client-install command was successful
```
This look less than 5 minutes, it should go by quick!

**One Time Password FreeIPA Client Installation and Configuration**

In the previous section, we installed a FreeIPA client directly from the compute node. We found the DNS and IPA server and entered our admin login to authorize the install. In this section, we'll notify the FreeIPA server of the new client first, give it a one time password, and then on the new client node we'll install with the password.

1. Client node requirements:

    a. /etc/hosts and hostnamectl is updated with a fully qualified domain name

    b. /etc/resolv.conf is updated with FreeIPA DNS nameserver IP

    c. epel and ipa-client is installed

    d. idm:DL1 module is enabled

2. On the FreeIPA server, add the future client node as a host. Use the --force to use a non-resolvable FQN --randomoption to generate a one-time random password for the enrollment.
```
# ipa host-add --force clientX.ipa.test --random

-----------------------------

Added host "clientX.ipa.test"

-----------------------------

Host name: clientX.ipa.test

Random password: 9FmbSqYMoWnFTilgY7TEV6O

Password: True

Keytab: False

Managed by: clientX.ipa.test
```
3. On the client node, install ipa client with the --password option to use the randomly generated password you just created for it
```
# ipa-client-install --uninstall --password=Password_String

This program will set up IPA client.

Version 4.9.11

Discovery was successful!

Do you want to configure chrony with NTP server or pool address? [no]:

Client hostname: client5.ipa.test

Realm: IPA.TEST

DNS Domain: ipa.test

IPA Server: eclusterX.ipa.test

BaseDN: dc=ipa,dc=test

Continue to configure the system with these values? [no]: yes

Synchronizing time

No SRV records of NTP servers found and no NTP server or pool address was provided.

Using default chrony configuration.

Attempting to sync time with chronyc.

Time synchronization was successful.

Do you want to download the CA cert from http://eradon2.ipa.test/ipa/config/ca.crt ?

(this is INSECURE) [no]: yes

Successfully retrieved CA cert

Subject:

Issuer:

CN=Certificate Authority,O=IPA.TEST

CN=Certificate Authority,O=IPA.TEST

Valid From: 2023-07-26 16:20:08

Valid Until: 2043-07-26 16:20:08

...

Client configuration complete.

The ipa-client-install command was successful
```
This took less than 10 minutes, it's super fast!

4. You can check all your hosts on the FreeIPA server node (and on the web UI)
```
# ipa host-find

---------------

3 hosts matched

---------------

Host name: client.ipa.test

Platform: x86_64

Operating system: 4.18.0-477.13.1.el8_8.x86_64

Principal name: host/client.ipa.test@IPA.TEST

Principal alias: host/client.ipa.test@IPA.TEST

SSH public key fingerprint: SHA256:mIE5xG/bC5OBTiFNZjbDHbEm6FdbBQlP77to82PG0Yc (ssh-ed25519),

SHA256:BeqEhLqGVH3tN52qr30TAs5ip1hl8y4FEl8kW1pg7PE (ecdsa-sha2-nistp256),

SHA256:qL60rRi3fII5W0I9lBNl+X0Vm6GJyUZfmMG//UnMU68 (ssh-rsa)

Host name: clientX.ipa.test

Principal name: host/client5.ipa.test@IPA.TEST

Principal alias: host/client5.ipa.test@IPA.TEST

SSH public key fingerprint: SHA256:am+VM5ha7AT1zy2pppeecK0Ul1cSOfa/Uk3j1MEs8d8 (ecdsa-sha2-nistp256), SHA256:9oZNQHZ+svaAeZ0RA/8IUxX07flwe1m9lGGL+SuiqqE (ssh-ed25519),

SHA256:LYCUdpxllWcDXoQlUBjrAYbUHKG72ReB5UrQqr1aXDU (ssh-rsa)

Host name: eclusterX.ipa.test

Principal name: host/eclusterX.ipa.test@IPA.TEST

Principal alias: host/eclusterX.ipa.test@IPA.TEST

SSH public key fingerprint: SHA256:G1ky5GBmLcQzdkxUFGbxM0s2yOUXa2dIhfBMcL8MDTA (ecdsa-sha2-nistp256), SHA256:TWSZKkJCr8fxUwd23DfKdsK97D5jdm4jx8W2PX08O8E (ssh-rsa),

SHA256:4gihgBH7NzY1eaYfpfgks9MQww4KAblehk1S7Bsg3cE (ssh-ed25519)

----------------------------

Number of entries returned 3

----------------------------
```
