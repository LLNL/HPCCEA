#!/usr/bin/python

import mysql.connector 
from mysql.connector import Error

def connectDatabase():


	#block tests if gender database exists already
	try:

	#connection set up using a password I created to run mysql on boron2
	#I think I want to look into making that passwordless

		mydb = mysql.connector.connect( host="localhost",user="root",password="Puffyf15", database="gender")
	
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

		sqlCommands = sqlFile.split(';')
		# Execute every command from the input file
		for command in sqlCommands:
   		# This will skip and report errors
			try:
        			cursor.execute(command)
    			except Error as e:
        			print "Command skipped: ", e
	return mydb
def insertGender(node_name,mydb):
	cluster = node_name[:-1]
	node_num = node_name[-1:]
	sql = "INSERT INTO NODE (cluster, node_num, node_name) VALUES (%s, %s, %s)"
	val = (cluster, node_num, node_name)
	cursor = mydb.cursor(buffered=True , dictionary=True)
	cursor.execute(sql, val)	
def main():

	mydb = connectDatabase()
	insertGender("practice1",mydb)

if __name__ == "__main__":
    main()
