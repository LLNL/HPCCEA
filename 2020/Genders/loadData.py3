#!/usr/bin/python

import mysql.connector 

#connection set up using a password I created to run mysql on boron2
#I think I want to look into making that passwordless
mydb = mysql.connector.connect( host="localhost",
  user="root",
  password="Puffyf15" )


cursor = mydb.cursor(buffered=True , dictionary=True)

# checks to see if gender database already exists
# creates if false
cursor.execute("SHOW DATABASES")
for x in cursor:
	if x['Database'] == 'gender':
		print("database already exists")
	
