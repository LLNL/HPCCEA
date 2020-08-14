#Test connecting to the database

import mysql.connector
def connectDatabase():
	with open('passW.txt') as f:
		password = [line.rstrip('\n') for line in f][0]
	print(password)
	config = {
		'user': 'root',
		'password': f'{password}', 
		'host': 'localhost',
		'database': 'gender', 
	}
	#mydb = mysql.connector.connect( host='localhost', user='root', password='{password}', database = 'gender')
	mydb = mysql.connector.connect(**config)
	cursor = mydb.cursor(buffered=True, dictionary=True)
	cursor.execute("SELECT * FROM NODE")
	print(cursor.fetchall())

connectDatabase()
