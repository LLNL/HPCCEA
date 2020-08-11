# Setting Password  
#### Password Set Up


` python3 -m gendersdb -password `
"Enter mysql password: " 

Now tool can be run "passwordlessly" by all users


# Populating Database
` python3 -m gendersdb -load `

This will comb through cfengine directory tree and pull all genders files. If an attribute for a node exists in a file but not in the database it will be inserted, if it exists but has a different value database will be updated, if it exists in both a file and database with the same value than it is ignored. If an attribute for a node is in the database but in no file than it is deleted from the dtabase.

# Adding a gender description 
` python3 -m gendersdb -descrip [gender] [description] `
Call this option with the gender and the description you want to add in for that gender. 

# Deleting the database
` python3 -m gendersdb -dd`
Use this option if you want to delete the entire database for some reason. 
 
