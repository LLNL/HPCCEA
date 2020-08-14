# Setting Password  
#### Password Set Up


` gendersdb -password `
"Enter mysql password: " 

Now tool can be run "passwordlessly" by all users


# Populating Database
` gendersdb -load `

This will comb through cfengine directory tree and pull all genders files. If an attribute for a node exists in a file but not in the database it will be inserted, if it exists but has a different value database will be updated, if it exists in both a file and database with the same value than it is ignored. If an attribute for a node is in the database but in no file than it is deleted from the dtabase.

# Adding a gender description 
` gendersdb -descrip [gender] [description] `
Call this option with the gender and the description you want to add in for that gender. 

# Deleting the database
` gendersdb -dd`
Use this option if you want to delete the entire database for some reason. 

# Querying options
` gendersdb -q [attr]`
This will return all of the nodes that have the specified attribute in hostlist formart. In addition in can be returned as 
comma seperated: -c 
space seperated: -s
newline seprated: -n

' gendersdb -Q [attr] `
Will set environment variables based on existance. If attr is in the database it will return 0, otherwise it will return 1 

#Additional modifications 
All of the above qeurying options can be modified to refine the query

` gendersdb -q [attr] -X [attr] `
This will return all of the nodes that have the specified attribute but not the other 

` gendersdb -q [attr] -XX [node] `
This will return all of the nodes that have a specified attribute but not be a particular node

` gendersdb -q -A `
This will return all of the attributes that exist in the database

#Getting values
` gendersdb -v [attr] [node]`
This will return all of the values of an attribute that exist on a node. If you do not pass a node name the local node will be assumed.

` gendersdb -V [attr] `
Will print all of the values of an attribute that exist on database.
` gendersdb -V -U [attr] `
Will only print unique values of an attribute that exist on databse.
` gendersdb -vv [attr] `
Same as -V exept that it prints the node name with it


