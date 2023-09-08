1. Configure your /etc/hosts and /etc/hostname in the node slightly differently. You're going to need a fully qualified domain name (FQDN), in order for DNS to work. For this ansible playbook to work, we'll need the domain to be 'ipa.test'.
```bash
#vi into /etc/hosts add the following line to the ip address of your node. Make sure the FQDN is listed first

192.168.xx.xx server.ipa.test server

#this command will change your hostname. You can also just vi into /etc/hostname and change directly

hostnamectl set-hostname server.ipa.test --static
```
After editing those files, it should save those changes without rebooting. Check your hostname like this:
```bash
[root@server ~]# hostname

server.ipa.test
```
2. Run the ansible script for installation with the following command:
```bash 
ansible-playbook ipa_install_DNS.yml
```
 
