#!/usr/bin/python

import mysql.connector 
from mysql.connector import Error

#block tests if gender database exists already
try:

#connection set up using a password I created to run mysql on boron2
#I think I want to look into making that passwordless

	mydb = mysql.connector.connect( host="localhost",
  	user="root",
  	password="Puffyf15" )
	
	if mydb.is_connected():
        	print('Connected to MySQL database')
		cursor = mydb.cursor(buffered=True , dictionary=True)

#if it does not exists runs createAll.sql script 
except Error as e:
	print(e)
	mydb = mysql.connector.connect( host="localhost", user="root", password="Puffyf15" )
	cursor = mydb.cursor(buffered=True , dictionary=True)
	cursor.execute("CREATE DATABASE gender")
