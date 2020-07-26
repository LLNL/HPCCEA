#!/usr/bin/python3

import os 
os.environ['PYTHONPATH'] = '/usr/local/lib64/python3.6/site-packages'
import argparse
parser = argparse.ArgumentParser("genders database query")

import genders 
gen = genders.Genders(filename="/etc/genders")

import mysql.connector
import hostlist

config = {
  'user': 'root',
  'password': 'nishappw', # EDIT WITH YOUR PASSWORD
  'host': 'localhost',
  'database': 'gender'
}

def parsequery(results):
	list = []
	for element in results:
		for e in element:
			if (e != None):
				list.append(e)
	return list

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()
group = parser.add_mutually_exclusive_group(required=False)
group.add_argument('-q', metavar='attr', help="Displays a hostrange of nodes that have the specified attribute.")
group.add_argument('-c', metavar='attr', help="Displays a comma separated list of nodes that have the specified attribute.")
group.add_argument('-n', metavar='attr', help="Displays a newline separated list  of nodes that have the specified attribute.")
group.add_argument('-s', metavar='attr', help="Displays a space separated list of nodes that have the specified attribute.")
group.add_argument('-v', nargs='+', metavar=('node', 'attr'), help="Returns any value associated with the attribute and the node.") 
group.add_argument('-V', metavar='attr', help="Prints all the values that exist for a specific attribute")
#parser.add_argument('-U', 
args = parser.parse_args()

def q_c_n_s_query(attr):
	query = ("SELECT node_name FROM CONFIGURATION WHERE gender_name=%s")
	cursor.execute(query, (attr,))
	results = cursor.fetchall()
	return parsequery(results)

if args.q != None:
	attr = args.q
	results = q_c_n_s_query(attr)
	if len(results) != 0:
		print(hostlist.compress_range(results))
elif args.c != None:
	results = q_c_n_s_query(args.c)
	if (len(results) != 0):
		print(hostlist.delimiter(results, ','))
elif args.n != None:
	results = q_c_n_s_query(args.n)
	if (len(results) != 0):
		print(hostlist.delimiter(results, '\n'))
elif args.s != None:
	results = q_c_n_s_query(args.s)
	if (len(results) != 0):
		print(hostlist.delimiter(results, ' '))
elif args.v != None:
	node = ""
	attr = ""
	if (len(args.v) == 1):
		node = gen.getnodename()
		attr = args.v[0]
	elif (len(args.v) == 2):
		node = args.v[0]
		attr = args.v[1]
	else:
		parser.error("Too many arguments.")
	query = ("SELECT val FROM CONFIGURATION WHERE node_name=%s && gender_name=%s")
	cursor.execute(query, (node, attr))
	results = cursor.fetchall()
	if len(results) == 0:
		parser.error("node or attribute not found")
	else:
		print(results[0][0])	
elif args.V != None:
	attr = args.V
	query = ("SELECT val FROM CONFIGURATION WHERE gender_name=%s")
	cursor.execute(query, (attr,))
	results = cursor.fetchall()
	results = parsequery(results)
	if len(results) != 0:
		print(hostlist.delimiter(results, '\n'))
cursor.close()
mydb.close()
