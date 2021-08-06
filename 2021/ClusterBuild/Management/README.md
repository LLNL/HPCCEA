# 2021 Cluster Build - Management nodes
Ansible code to automate the install of management nodes

To use this code you will need to modify playbooks and template file that have specific details used in the HPCCEA environment.  For example:

- custom_management.sh
- add_hosts.yml
- address_dict.yml
- dhcp.conf.j2
- setup_networkscripts.yml

