#!/bin/bash

hostname=$(hostname)
domain=${hostname::-1}  # Removes the last character from the hostname

ansible-playbook nfs_setup.yml --extra-vars "domain=$domain" --limit=$1

