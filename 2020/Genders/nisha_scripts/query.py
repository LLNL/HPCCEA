#!/usr/bin/python3
import sys
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
  'password': 'nishappw',  # EDIT WITH YOUR PASSWORD
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

def printquery(results):
        for element in results:
                for e in element:
                        if (e != None):
                                print(e)

def regex(cluster):
	regex = '' 
	for char in cluster:
		regex += '[' + char + ']'
	regex += '[0-9]'
	return regex

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()
group = parser.add_mutually_exclusive_group(required=False)

group.add_argument('-q', metavar='attr', help="displays a hostrange of nodes that have the specified attribute.")

group.add_argument('-c', metavar='attr', help="displays a comma separated list of nodes that have the specified attribute.")

group.add_argument('-n', metavar='attr', help="displays a newline separated list  of nodes that have the specified attribute.")

group.add_argument('-s', metavar='attr', help="displays a space separated list of nodes that have the specified attribute.")

group.add_argument('-v', nargs='+', metavar=('node', 'attr'), help="returns any value associated with the attribute and the node.") 

group.add_argument('-Q', nargs='+', metavar=('node', 'attr'), help="returns 0 to the environment if the conditions are met; 1 otherwise") 

group.add_argument('-V', metavar='attr', help="prints all the values that exist for a specific attribute")
#parser.add_argument('-U', 

group.add_argument('-l', nargs='*', metavar='node', help='prints all the attributes/values associated with the node. if no node is specified, all of the attributes are listed.')

args = parser.parse_args()

def c_n_s_query(attr):
	query = ("SELECT node_name FROM CONFIGURATION WHERE gender_name=%s")
	cursor.execute(query, (attr,))
	results = cursor.fetchall()
	return parsequery(results)

def parsedefault(inp):
	if (len(inp) == 1):
		node = gen.getnodename()
		attr = inp[0]
	elif (len(inp) == 2):
		node = inp[0]
		attr = inp[1]
	else:
		parser.error("Too many arguments.")
	return node, attr

if args.q != None:
	attr = args.q
	nodes  = c_n_s_query(attr)
	if len(nodes) != 0:	
		clusters = []
		for node in nodes:
			clust = node[0:len(node)-1]
			clust += '%'
			if not (clust in clusters):
				clusters.append(clust)
				query = ('SELECT node_name FROM CONFIGURATION  WHERE node_name LIKE %s && gender_name=%s')
				cursor.execute(query, (clust, attr))
				results = parsequery(cursor.fetchall())
				print(hostlist.compress_range(results))
elif args.c != None:
	results = c_n_s_query(args.c)
	if (len(results) != 0):
		print(hostlist.delimiter(results, ','))
elif args.n != None:
	results = c_n_s_query(args.n)
	if (len(results) != 0):
		print(hostlist.delimiter(results, '\n'))
elif args.s != None:
	results = c_n_s_query(args.s)
	if (len(results) != 0):
		print(hostlist.delimiter(results, ' '))
elif args.v != None:
	node, attr = parsedefault(args.v)
	query = ("SELECT val FROM CONFIGURATION WHERE node_name=%s && gender_name=%s")
	cursor.execute(query, (node, attr))
	results = cursor.fetchall()
	if len(results) == 0:
		parser.error("node or attribute not found")
	else:
		print(results[0][0])		
elif args.Q != None:
	node, attr = parsedefault(args.Q)
	query = ("SELECT node_name FROM CONFIGURATION WHERE node_name=%s && gender_name=%s")
	cursor.execute(query, (node,attr))
	results = cursor.fetchall()
	print(len(results))
	if len(results) == 0:
		sys.exit(1)
	else:
		sys.exit(0)
elif args.V != None:
	attr = args.V
	query = ("SELECT val FROM CONFIGURATION WHERE gender_name=%s")
	cursor.execute(query, (attr,))
	results = cursor.fetchall()
	results = parsequery(results)
	if len(results) != 0:
		print(hostlist.delimiter(results, '\n'))
# Implement -U
elif args.l != None:
	if len(args.l) > 1:
		parser.error("too many arguments")
	if len(args.l) == 0:
		query = ("SELECT gender_name FROM GENDER")
		cursor.execute(query)
		printquery(cursor.fetchall())
		sys.exit(0)
	node = args.l[0]
	query = ("SELECT gender_name, val FROM CONFIGURATION WHERE node_name=%s")
	cursor.execute(query, (node,))
	for gender_name, val in cursor:
		if val == None:
			print(gender_name)
		else:
			print(gender_name + "=" + val)
cursor.close()
mydb.close()
