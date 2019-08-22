#!/bin/bash
#this script grabs all user accounts on the system and generates the .s3cfg file
#and as well as a ceph account for each user and places the .s3cfg in the users
#home directory

#create the arrays to hold all sets of accounts
declare -a rmusers #users to be removed
declare -a cephusers #users with ceph accounts
declare -a sysusers #users on the computer

#grab all of the users accounts on the system
sysusers="$(awk -F':' '{ if ( $3 >= 1000 && $3 < 65000 ) print $1 }' /etc/passwd)"

#read all of the current ceph user accounts
while read user; do
	#cut out the extra characters and store the usernames in an array
	if [[ "$user" != "["  &&  "$user" != "]" ]]; then
		curuser=$(echo $user | cut -d '"' -f 2)
		cephusers+=$curuser
		cephusers+=" "

		#check to see if any ceph users no longer have user accounts on the system
 		counter=0
		c=0

		#compare the current user to all the system users
		for u in $sysusers; do
			if [ "$u" != "$curuser" ]; then
				counter=$((counter+1))
			fi

			c=$((c+1))
		done
		
		#if the counters are equal (the ceph user doesn't have an account
		#on the system) add the user to the array of users to be removed
		if [[ $counter == $c ]]; then
			rmusers+=$curuser
			rmusers+=" "
		fi
			
	fi

done < <(radosgw-admin user list)

#remove the users that no longer have account on the system 
for u in $rmusers; do
	echo "Would you like to delete the data for user: $u"
	echo "(Y)es or (N)o"
	torm="y"
	read torm

	#this feature requires a user by the name of "admin-ceph"
	#if this user is not on the system create it first	
	#if the admin wants to remove the user's data
	#delete the user and their data
	if [[ "$torm" == "y" || "$torm" == "Y" ]]; then
		radosgw-admin user rm --purge-data --uid=$u 
	fi

	#if the admin wants to save the user's data 
	#move all of the buckets to the control of the admin
	if [[ "$torm" == "n" || "$torm" == "N" ]]; then
		if (( $(radosgw-admin bucket stats --uid=a | wc -l) > 1 )); then

			while read line; do
				if [[ $line == *id* ]]; then
					buck_id=$( echo $line | cut -d '"' -f 4 )
				fi

				if [[ $line == *bucket* && $line != *bucket_quota* ]]; then
					buck_name=$( echo $line | cut -d '"' -f 4 )
				fi
				
				#allow for multiple buckets per user to be transferred to the admin
				if [[ $line == "}," && $prevline == "}" ]]; then	
					radosgw-admin bucket unlink --bucket-id=$buck_id --bucket=$buck_name --uid=$u
					radosgw-admin bucket link --bucket-id=$buck_id --bucket=$buck_name --uid=admin-ceph	
				fi

				prevline=$line
			done < <(radosgw-admin bucket stats --uid=$u)
		fi
	
		radosgw-admin bucket unlink --bucket-id=$buck_id --bucket=$buck_name --uid=$u
		radosgw-admin bucket link --bucket-id=$buck_id --bucket=$buck_name --uid=admin-ceph	
		
		#once all of the user's buckets have been linked to the admin
		#remove the user
		radosgw-admin user rm --uid=$u
	fi

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

#tabstop=2
