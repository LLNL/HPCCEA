#!/usr/bin/python

import genders;
import mysql.connector 
from mysql.connector import Error

#sets up connection to genders database
def connectDatabase():

	#block tests if gender database exists already
	try:

	#connection set up using a password I created to run mysql on boron2
	#I think I want to look into making that passwordless since this would
	#only work on boron2

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

#looks through given genders file and parses node information.
#if gender already exists on the node it does not insert
def parse_file(filename):
	gens = genders.Genders(filename="gentestfi.txt")


#debugging function. prints all nodes and genders on nodes
def print_all(mydb):
	sel = "SELECT * FROM CONFIGURATION"
	cur = mydb.cursor()
	cur.execute(sel)
	records = cur.fetchall()
	for row in records:
		print(row)

def insertNode(node_name,mydb):
	cluster = node_name[:-1]
	node_num = node_name[-1:]
	sql = "INSERT INTO NODE (cluster, node_num, node_name) VALUES (%s, %s, %s)"
	val = (cluster, node_num, node_name)
	cursor = mydb.cursor(buffered=True , dictionary=True)
	cursor.execute(sql, val)

def insertGender(gender_name,descrip,mydb):
	sql = "INSERT INTO GENDER(gender_name,descrip) VALUES (%s,%s)"
	val = (gender_name,descrip)
	cur = mydb.cursor(buffered=True, dictionary=True)
	cur.execute(sql,val)
	

def insertConfig(val, node_name, gender_name, mydb):
	config_id = node_name + gender_name
	sql = "INSERT INTO CONFIGURATION(config_id,val,node_name,gender_name) VALUES (%s,%s,%s,%s)"
	val = (config_id,val,node_name,gender_name)
	cur = mydb.cursor(buffered=True, dictionary=True)
	cur.execute(sql,val)

def main():

	mydb = connectDatabase()
	insertNode("practice1",mydb)
	insertGender("pretend_name","description",mydb)
	insertConfig("val", "practice1", "pretend_name", mydb)
	print_all(mydb)
if __name__ == "__main__":
    main()
