#!/bin/bash
#this script grabs all user accounts on the system and generates the .s3cfg file
#and as well as a ceph account for each user and places the .s3cfg in the users
#home directory

#grab all of the users accounts on the system
sysusers="$(awk -F':' '{ if ( $3 >= 1000 && $3 < 65000 ) print $1 }' /etc/passwd)"

#read all of the current ceph user accounts
while read user
do
  #cut out the extra characters and store the usernames in an array
  if [[ "$user" != "["  &&  "$user" != "]" ]]; then
    cephusers+=$( echo $user | cut -d '"' -f 2 )

	#check to see if any ceph users no longer have user accounts on the system
    if [[ !( "${sysusers[*]}" =~ "$( echo user | cut -d '"' -f 2 )" ) ]]; then
      rmusers+=$( echo $user | cut -d '"' -f 2 )
    fi
  fi
done < <(radosgw-admin user list)

#remove the users that no longer have account on the system as well 
#as their data
for u in $rmusers; do
  radosgw-admin user rm --purge-data --uid=$u
done

#grab the access and secret keys for all the users on the system
for u in $sysusers; do

  #if the user is new ie. doesn't have a current ceph account
  #create the user and grab the keys
  if [[ !( "${cephusers[*]}" =~ "$u" ) ]]; then
    while read key; do
      if [[ $key == *access_key* ]]; then
        acc_key=$( echo $key | cut -d '"' -f 4)
      fi
      if [[ $key == *secret_key* ]]; then
        sec_key=$( echo $key | cut -d '"' -f 4)
      fi
    done < <(radosgw-admin user create --uid=$u --display-name=$u)
  
  #if the is returning get their info
  else
	#grab the users old access and secret keys
    while read key; do
      if [[ $key == *access_key* ]]; then
		acc_key=$( echo $key | cut -d '"' -f 4 )
      fi
      if [[ $key == *secret_key* ]]; then
		sec_key=$( echo $key | cut -d '"' -f 4)
      fi
	done < <(radosgw-admin key user info --uid=$u)
	
	#remove the users old keys and generate a new pair
	radosgw-admin key rm --purge-keys --uid=$u --access_key=$acc_key --secret_key=$sec_key
	radosgw-admin key create --uid=$u --gen-access-key --gen-secret  

	#grab the users new keys
	while read key; do
      if [[ $key == *access_key* ]]; then
        acc_key=$( echo $key | cut -d '"' -f 4 )
      fi
      if [[ $key == *secret_key* ]]; then
        sec_key=$( echo $key | cut -d '"' -f 4)
      fi
    done < <(radosgw-admin key user info --uid=$u)
  fi
	
  #if the user has a home directory already configure s3cmd and place the file in their home directory
  if [[ -d /home/$u ]]; then
    s3cmd --configure --no-ssl --no-encrypt --config=/home/$u/.s3cfg --secret_key=$sec_key --access_key=$acc_key --host=exenon5 --host-bucket="%(bucket)s.exenon5" --dump-config 2>&1 | tee /home/$u/.s3cfg
  
  #if not create the directoy, change the owner, and then configure s3cmd
  #and place the file in their home directory
  else
    mkdir /home/$u
    chown $u:$u /home/$u
    s3cmd --configure --no-ssl --no-encrypt --config=/home/$u/.s3cfg --secret_key=$sec_key --access_key=$acc_key --host=exenon5 --host-bucket="%(bucket)s.exenon5" --dump-config 2>&1 | tee /home/$u/.s3cfg
  fi

done
