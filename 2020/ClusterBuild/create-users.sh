#!/bin/bash

username=$1
password=$2
groupid=$3
userid=$4
node=$5
mgmt=$6

ansible-playbook user_setup_host.yml --extra-vars "username=$username pass=$password groupid=$groupid userid=$userid" --limit=$mgmt

ansible-playbook user_setup_host.yml --extra-vars "username=$username pass=$password groupid=$groupid userid=$userid" --limit=$node

ansible-playbook user_setup_mgmt.yml --extra-vars "username=$username pass=$password node=$node"
