#!/usr/bin/python3
import pdb
import os
os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'

#LD_LIBRARY_PATH needs to be set outside the python shell
os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'

import genders

def parseName(node_name): 
	node_num = node_name[-1]
	cluster = node_name[0:len(node_name)-1]	
	return node_num, cluster

import mysql.connector

config = {
  'user': 'root',
  'password': 'nishappw', # EDIT WITH YOUR PASSWORD
  'host': 'localhost',
  'database': 'gender'
}

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

def node(dest):
	gen = genders.Genders(filename=dest)
	for node_name in gen.getnodes():
		node_name_query = ("SELECT node_name FROM NODE WHERE node_name=%s")
		cursor.execute(node_name_query, (node_name,))
		result = cursor.fetchall()
		if len(result) == 0:
			node_num, cluster = parseName(node_name)
			add_node = ("INSERT IGNORE INTO NODE (node_name, node_num, cluster) VALUES (%s, %s, %s)")
			cursor.execute(add_node, (node_name, node_num, cluster))
			mydb.commit()

def gender(dest):
	gen = genders.Genders(filename=dest)
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
def configuration(dest):
	gen = genders.Genders(filename=dest)
	for node in gen.getnodes(): 
		for attribute in gen.getattr(node):
			config_id = node + attribute
			value = gen.getattrval(attribute, node)
			config_query = ("SELECT config_id, val FROM CONFIGURATION WHERE config_id=%s")
			cursor.execute(config_query, (config_id,))
			result = cursor.fetchall()
			if len(result) == 0: 
				add_config = ("INSERT IGNORE INTO CONFIGURATION (config_id, val, node_name, gender_name) VALUES (%s, %s, %s, %s)")
				cursor.execute(add_config, (config_id, value, node, attribute))
				mydb.commit()
			else: 
				for (config_id, val) in result:
					if  val == value: 
						break;
					update_config = ("UPDATE CONFIGURATION SET val=%s WHERE config_id=%s")
					cursor.execute(update_config, (value, config_id))
					mydb.commit()

def deletenodes(dest, present, absent):
	gen = genders.Genders(filename=dest)
	node_query = ("SELECT node_name FROM NODE")
	cursor.execute(node_query)
	for (node_name,) in cursor: 
		if gen.isnode(node_name) == 1:
			if not node_name in present:
				present.append(node_name)
			if node_name in absent:
				absent.remove(node_name)
		elif (not node_name in present) and (not node_name in absent):
			absent.append(node_name)

def deleteattrs(dest, present, absent):
        gen = genders.Genders(filename=dest)
        node_query = ("SELECT gender_name FROM GENDER")
        cursor.execute(node_query)
        for (gender_name,) in cursor:
                if gen.isattr(gender_name) == 1:
                        if not gender_name in present:
                                present.append(gender_name)
                        if gender_name in absent:
                                absent.remove(gender_name)
                elif (not gender_name in present) and (not gender_name in absent):
                        absent.append(gender_name)

# other idea - create set of nodes that exist currently, take difference with all items in database, delete the difference 
def deleteconfig(dest):
	gen = genders.Genders(filename=dest)
	for node in gen.getnodes():
		query = ("SELECT gender_name, val FROM CONFIGURATION WHERE node_name=%s")
		cursor.execute(query, (node,))
		results = cursor.fetchall() 
		for (gender_name, val) in results: 
			if (val == None) and gen.testattr(gender_name, node) == 0: 
				query = ("DELETE FROM CONFIGURATION WHERE config_id=%s")
				cursor.execute(query, (node + gender_name,))
				mydb.commit()
			elif not (val == None) and gen.testattrval(gender_name, val, node) == 0:
				if gen.testattr(gender_name, node) == 0: 
					query = ("DELETE FROM CONFIGURATION WHERE config_id=%s")
					cursor.execute(query, (node + gender_name,))
					mydb.commit()

def __main__(dest):
	node(dest)
	gender(dest)
	configuration(dest)
	deleteconfig(dest)

import shutil

os.system("ls -d ~/cfengine/clusters/*/genders > pathfile.txt")
file_object = open('pathfile.txt', 'a')
file_object.write('/etc/genders')
file_object.close()

with open("pathfile.txt", "r") as pathfile:
	nodes, deletenodeslist = [], []
	genderslist, deletegenders = [], []
	for line in pathfile:
		line = line.strip() 
		dest = "tempfile.txt"
		shutil.copyfile(line, dest)
		__main__(dest)
		deletenodes(dest, nodes, deletenodeslist)
		deleteattrs(dest, genderslist, deletegenders) 
	query = ("DELETE FROM NODE WHERE node_name=%s")
	for node in deletenodeslist:
		cursor.execute(query, (node,))
		mydb.commit()
	query = ("DELETE FROM GENDER WHERE gender_name=%s")
	for gender in deletegenders:
		cursor.execute(query, (gender,))
		mydb.commit()

os.remove("pathfile.txt")
os.remove("tempfile.txt")
cursor.close()
mydb.close()
