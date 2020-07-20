#!/usr/bin/python3

import os
os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

import genders
gen = genders.Genders(filename="/etc/genders")

def parseName(node_name): 
	node_num = node_name[-1]
	cluster = node_name[0:len(node_name)-1]	
	return node_num, cluster

import mysql.connector

config = {
  'user': 'root',
  'password': 'nishappw',
  'host': 'localhost',
  'database': 'genders'
}

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

# GAME PLAN
# Check in the node table - does this node exist there 
# If not, insert 
node_name = gen.getnodename();
#node_num, cluster = parseName(node_name)

node_name_query = ("SELECT node_name FROM NODE WHERE node_name=%s")
cursor.execute(node_name_query, (node_name,))
result = cursor.fetchall()
if len(result) == 0:
	node_num, cluster = parseName(node_name)
	add_node = ("INSERT INTO NODE (node_name, node_num, cluster) VALUES (%s, %s, %s)")
	cursor.execute(add_node, (node_name, node_num, cluster))
	mydb.commit()

cursor.close()
mydb.close()

