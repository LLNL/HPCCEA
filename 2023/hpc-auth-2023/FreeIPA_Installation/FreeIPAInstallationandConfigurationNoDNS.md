<a name="br1"></a> 

**Free-IPA Installation and Configuration**

**References**

[**FreeIPA Quickstart Guide**](https://freeipa.org/page/Quick_Start_Guide#getting-started-with-ipa)

[**Rocky Linux Install**](https://computingforgeeks.com/install-and-configure-freeipa-server-on-rocky-linux/)

[**Client Installation**](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/5/html/configuring_identity_management/installing_the_ipa_client_on_linux)

[**Creating a FreeIPA TOTP**](https://freeipa.org/page/V4/OTP#self-managed-tokens)

**Free-IPA Server Installation on Compute Node (do this as root)**

1\. Install and enable some dependencies.
```bash
dnf install epel-release

dnf module enable idm:DL1
```

2\. Disable firewalld. This will open necessary ports for FreeIPA to run through.
```bash
systemctl stop firewalld

systemctl disable firewalld
```

3\. Configure your /etc/hosts and /etc/hostname IN THE COMPUTE NODE slightly differently. You're going to need a fully qualified domain name (FQDN), in order for DNS to work.
```bash
#vi into /etc/hosts add the following line to the ip address of your node. Make sure the FQDN is listed first

192.168.95.x {eclusterx}.ipa.test esiliconx ex

#this command will change your hostname. You can also just vi into /etc/hostname and change directly

hostnamectl set-hostname {eclusterx}.ipa.test --static
```

After editing those files, reboot the node and it should save those changes. When you re-enter the node, check your hostname like this:
```bash
[root@clusterx ~]# hostname

eclusterx.ipa.test
```

4\. Install the server material with this command.
```bash
dnf install ipa-server
```

5\. Configure the server with this command. Answer the following prompts accordingly. When it is blank, that means hit 'enter' for the default.
```bash
ipa-server-install

The log file for this installation can be found in /var/log/ipaserver-install.log

\==============================================================================

This program will set up the IPA Server.

Version 4.9.11

This includes:

\* Configure a stand-alone CA (dogtag) for certificate management

\* Configure the NTP client (chronyd)

\* Create and configure an instance of Directory Server

\* Create and configure a Kerberos Key Distribution Center (KDC)

\* Configure Apache (httpd)

\* Configure SID generation

\* Configure the KDC to enable PKINIT

To accept the default shown in brackets, press the Enter key.



Do you want to configure integrated DNS (BIND)? [no]:

Enter the fully qualified domain name of the computer

on which youre setting up server software. Using the form

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

Trust is configured but no NetBIOS domain name found, setting it now.

Enter the NetBIOS name for the IPA domain.

Only up to 15 uppercase ASCII letters, digits and dashes are allowed.

Example: EXAMPLE.

NetBIOS domain name [IPA]:

Do you want to configure chrony with NTP server or pool address? [no]:

The IPA Master Server will be configured with:

Hostname:

eclusterx.ipa.test

IP address(es): 192.168.95.x

Domain name:

Realm name:

ipa.test

IPA.TEST

The CA will be configured with:

Subject DN:

CN=Certificate Authority,O=IPA.TEST

Subject base: O=IPA.TEST

Chaining:

self-signed

Continue to configure the system with these values? [no]: yes

The following operations may take some minutes to complete.

Please wait until the prompt is returned.
```

Be patient, as the installation may take fairly long. You'll know if the installation was successful if the following line looks like this:
```bash
The ipa-server-install command was successful
```

**Using the Web UI as Admin (do this as user)**



<a name="br3"></a> 

1\. Run the following command in both your management and your compute node. This downloads firefox, xauth, and xterm, which will allow the compute node to access the local https network.
```bash
dnf install -y firefox xauth xterm
```

2\. Switch to your user rather than running on root. Make sure that your administrative ticket is valid and running with this command. You should get prompted for the password you set. After that, print the ticket with the next command.
```bash
#this will make the ticket and prompt for the password

kinit admin

#this will print the ticket

klist
```

3\. Enter a VNC window. This will allow you to be able to view your page. Within the VNC, ssh into lgw2-pub with your user. From there, we're gonna specify the xauth permissions with the -X tag when we ssh.
```bash
#first, ssh into management from lgw2-pub

ssh -X user@clusteri

#check if xterm works

xterm

#close that window and ssh into the compute node that is running the ipa server

ssh -X user@ex

#check if xterm works

xterm

#if it works bring up a firefox window

firefox --no-remote
```
4\. Within that firefox window type in the domain name you set up (ex. <https://eclusterx.ipa.test)>. You should be able to see your window!

**FreeIPA Client Installation and Configuration**

1\. Select a different compute node than the one running the IPA server. To begin, follow a similar format of installing dependencies and disabling firewalls:
```bash
#installing dependencies

dnf install epel-release

dnf module enable idm:DL1

dnf install ipa-client

#disabling firewalls

systemctl stop firewalld

systemctl disable firewalld
```

2\. Change your hostname to another fully qualified hostname. (example: client.ipa.test)
```bash
#vi into /etc/hosts add the following line to the ip address of your node. Make sure the FQDN is listed first

192.168.95.x client.ipa.test esiliconx ex

#this command will change your hostname. You can also just vi into /etc/hostname and change directly

hostnamectl set-hostname client.ipa.test --static
```

3\. Edit your /etc/resolv.conf file to point to your DNS server. This allows the NetworkManager to find your ipa-server. If you chose to [integrate DNS with your ipa server](https://lc.llnl.gov/confluence/pages/viewpage.action?pageId=753196798), then merely point the nameserver to the IP of that node. If you didn't you'll have to make a DNS server within the domain of both your client and ipa-server, which can be done easily on your management node. Here is the [tutorial](https://lc.llnl.gov/confluence/display/HPCCEA/Configure+a+dnsmasq+Server) on how to configure a dnsmasq server.
```bash
#vi into /etc/resolv.conf and make it look like this

nameserver 192.168.95.x #the IP address of your DNS server

search ipa.test #the domain of your server DNS. Should be ipa.test if you followed this tutorial example
```

Test that you can dig or nslookup your ipa-server.
```bash
#this command tries to find this domain name

nslookup eclusteri.ipa.test

#once it's found, it will give you information similar to this

Server:

Address:

192.168.95.1

192.168.95.1#53

Name:

eclusteri.ipa.test

Address: 192.168.95.x
```

4\. Next we will go through with the client configuration. Answer the prompts accordingly:

```bash
ipa-client-install

This program will set up IPA client.

Version 4.9.11

DNS discovery failed to determine your DNS domain

Provide the domain name of your IPA server (ex: example.com): ipa.test

Provide your IPA server name (ex: ipa.example.com): eclusteri.ipa.test

The failure to use DNS to find your IPA server indicates that your resolv.conf file is not properly

configured.

Autodiscovery of servers for failover cannot work with this configuration.

If you proceed with the installation, services will be configured to always access the discovered server

for all operations and will not fail over to other servers in case of failure.

Proceed with fixed values and no DNS discovery? [no]: yes

Do you want to configure chrony with NTP server or pool address? [no]:

Client hostname: client.ipa.test

Realm: IPA.TEST

DNS Domain: ipa.test

IPA Server: eclusteri.ipa.test

BaseDN: dc=ipa,dc=test

Continue to configure the system with these values? [no]: yes

Synchronizing time

No SRV records of NTP servers found and no NTP server or pool address was provided.

Using default chrony configuration.

Attempting to sync time with chronyc.

Time synchronization was successful.

User authorized to enroll computers: admin

Password for admin@IPA.TEST: #enter the password you set up for the ipa-server

Successfully retrieved CA cert

Subject:

Issuer:

CN=Certificate Authority,O=IPA.TEST

CN=Certificate Authority,O=IPA.TEST

Valid From: 2023-07-21 20:54:56

Valid Until: 2043-07-21 20:54:56

Enrolled in IPA realm IPA.TEST

Created /etc/ipa/default.conf

Configured /etc/sssd/sssd.conf

Systemwide CA database updated.

Adding SSH public key from /etc/ssh/ssh_host_ecdsa_key.pub

Adding SSH public key from /etc/ssh/ssh_host_ed25519_key.pub

Adding SSH public key from /etc/ssh/ssh_host_rsa_key.pub

Could not update DNS SSHFP records.

SSSD enabled

Configured /etc/openldap/ldap.conf

Unable to find 'admin' user with 'getent passwd root@ipa.test'!

Unable to reliably detect configuration. Check NSS setup manually.

Configured /etc/ssh/ssh_config

Configured /etc/ssh/sshd_config

Configuring ipa.test as NIS domain.

Configured /etc/krb5.conf for IPA realm IPA.TEST

Client configuration complete.

The ipa-client-install command was successful
```

**Using the Client Web UI as a User (do this as user)**

1\. First, make sure that you have a user you can log into the ipa-server with. Enter the ipa-server node and you can create one on the command line, or within the ipa-server Web UI. Do so by clicking the 'add' button.

2\. After you've created a user, enter the client server node. Create a user ticket by running this command with the username you created in Step 1. You should get prompted for the password you set. It will also prompt you to reset your password, which is a standard for ipa. After that, print the ticket with the next command.
```bash
#this will make the ticket and prompt for the password

kinit cancy

Password for cancy@IPA.TEST:

Password expired. You must change it now.

Enter new password:

Enter it again:

#this will print the ticket

klist
```

3\. Enter a VNC window. This will allow you to be able to view your page. Within the VNC, ssh into lgw2-pub with your user. From there, we're gonna specify the xauth permissions with the -X tag when we ssh.
```bash
#first, ssh into management from lgw2-pub

ssh -X user@clusteri

#check if xterm works

xterm

#close that window and ssh into the compute node that is running the ipa server

ssh -X user@ex

#check if xterm works

xterm

#if it works bring up a firefox window

firefox --no-remote
```

4\. Within that firefox window type in the domain name you set up (ex. [https://cancy35.ipa.test)](https://eclusterx.ipa.test\)). You should be able to see your window! Login as the user you just created.

5\. You should be brought to a page that views your information, with the ability to edit it, as so. Congratulations! You have a client server, an ipa-server, and a user. There is now a world of possibilities for adding users, groups, setting up 2FA with google auth, and much more!

[**Setting Up 2FA for your User**](https://lc.llnl.gov/gitlab/acosta19/hpc-auth-2023/-/blob/main/WebUI%20Documentation/SettingUp2FAforFreeIPAUser.md)

