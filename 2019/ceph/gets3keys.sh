#!/bin/bash
#this script will parse through the users and grab their 
#public and private keys in order to use the python boto
#library to connect to the ceph server

#if the keys.txt file exists, remove it
if [[ -f keys.txt ]]; then 
  sudo rm -f keys.txt
fi

echo '-- Listing All Ceph Users --'

#read all ceph rgw users one at a time
while read USER
do
  #cut out extra characters and make sure only 
  #ceph rgw users show up
  if [[ "$USER" != "["  &&  "$USER" != "]" ]]; then
    if [[ "${USER: -1}" == , ]]; then
      USER="${USER::-1}"
    fi
    echo "$USER"
  fi

#feed in the command to list the users
done < <(sudo radosgw-admin user list)

#prompt the user for which rgw user they want to use
echo "Which user would you like to use to access the ceph server?"
echo "Enter the name of the user followed by [ENTER]"

read user

#read the user info
while read line
do
  #pull out both keys and write them to a file
  if [[ $line == *access_key* || $line == *secret_key* ]]; then
    key=$( echo $line | cut -d '"' -f 4)
    echo "$key" >> keys.txt
  fi

#feed in the user info command 
done < <(sudo radosgw-admin user info --uid=$user)
