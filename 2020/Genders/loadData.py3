#!/usr/bin/python

import mysql.connector 
from mysql.connector import Error

#block tests if gender database exists already
try:

#connection set up using a password I created to run mysql on boron2
#I think I want to look into making that passwordless

	mydb = mysql.connector.connect( host="localhost",
  	user="root",
  	password="Puffyf15", database="gender")
	
	if mydb.is_connected():
        	print('Connected to MySQL database')
		cursor = mydb.cursor(buffered=True , dictionary=True)

#if it does not exists runs createAll.sql script 
except Error as e:
	print(e)
	mydb = mysql.connector.connect( host="localhost", user="root", password="Puffyf15" )
	cursor = mydb.cursor(buffered=True , dictionary=True)
	# Open and read the file as a single buffer
	fd = open('createALL.sql', 'r')
	sqlFile = fd.read()
	fd.close()

	# all SQL commands (split on ';')
	sqlCommands = sqlFile.split(';')
	# Execute every command from the input file
	for command in sqlCommands:
   	# This will skip and report errors
    	# For example, if the tables do not yet exist, this will skip over
    	# the DROP TABLE commands
		try:
        		cursor.execute(command)
    		except Error as e:
        		print "Command skipped: ", e
#	cursor = mydb.cursor(buffered=True , dictionary=True)
#	cursor.execute("CREATE DATABASE gender")
#sql = "DROP DATABASE gender"
#cursor.execute(sql)
