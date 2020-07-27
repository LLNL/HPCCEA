#!/usr/bin/python3

# UPDATE -------
# Don't need this, will be done in the driver script.
#import os
#os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'
#os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

# Reads data from a genders file at /etc/genders and inserts it into the "gender" database

import genders
gen = genders.Genders(filename="/etc/genders")

def parseName(node_name): 
	node_num = node_name[-1]
	cluster = node_name[0:len(node_name)-1]	
	return node_num, cluster

import mysql.connector

config = {
  'user': 'root',
  'password': # EDIT WITH YOUR PASSWORD
  'host': 'localhost',
  'database': 'gender'
}

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

# NODE 
for node_name in gen.getnodes():
	node_name_query = ("SELECT node_name FROM NODE WHERE node_name=%s")
	cursor.execute(node_name_query, (node_name,))
	result = cursor.fetchall()
	if len(result) == 0:
		node_num, cluster = parseName(node_name)
		add_node = ("INSERT IGNORE INTO NODE (node_name, node_num, cluster) VALUES (%s, %s, %s)")
		cursor.execute(add_node, (node_name, node_num, cluster))
		mydb.commit()

# GENDER
for attr in gen.getattr_all():
	gender_query = ("SELECT gender_name from GENDER where gender_name=%s")
	cursor.execute(gender_query, (attr,))
	result = cursor.fetchall()
	if len(result) == 0:
		descrip = None 
		add_gender = ("INSERT IGNORE INTO GENDER (gender_name, descrip) VALUES (%s, %s)")
		cursor.execute(add_gender, (attr, descrip))
		mydb.commit()	

# CONFIGURATION 
for node in gen.getnodes(): 
	for attribute in gen.getattr(node):
		config_id = node + attribute
		value = gen.getattrval(attribute, node)
		config_query = ("SELECT config_id, val FROM CONFIGURATION WHERE config_id=%s")
		cursor.execute(config_query, (config_id,))
		if cursor.rowcount == 0:
			result = cursor.fetchall()
			add_config = ("INSERT IGNORE INTO CONFIGURATION (config_id, val, node_name, gender_name) VALUES (%s, %s, %s, %s)")
			cursor.execute(add_config, (config_id, value, node, attribute))
			mydb.commit()
			continue
		for (config_id, val) in cursor:
			if  val == value: 
				break;
			update_config = ("UPDATE CONFIGURATION SET val=%s WHERE config_id=%s")
			cursor.execute(update_config, (value, config_id))
			mydb.commit()
cursor.close()
mydb.close()
