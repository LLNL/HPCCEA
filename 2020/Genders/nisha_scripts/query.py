#!/usr/bin/python3
import pdb
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
  'password': 'MyNewPass',  # EDIT WITH YOUR PASSWORD
  'host': 'localhost',
  'database': 'gender'
}
import numpy as np

#def parsequery(results):
#	list = []
#	for element in results:
#		for e in element:
#			if (e != None):
#				list.append(e)
#	return list

def printquery(results):
        for element in results:
                for e in element:
                        if (e != None):
                                print(e)

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

mgroup = parser.add_mutually_exclusive_group()
qgroup = parser.add_mutually_exclusive_group()

mgroup.add_argument('-q', nargs='*', metavar='attr', help="displays a hostrange of nodes that have the specified attribute.")

qgroup.add_argument('-A', help="Prints out all nodes in the database.", action="store_true")

qgroup.add_argument('-X', metavar='exclude query', help='Excludes the results of the given query.')

mgroup.add_argument('-c',nargs = '*',metavar='attr', help="displays a comma separated list of nodes that have the specified attribute.")

mgroup.add_argument('-n',nargs='*', metavar='attr', help="displays a newline separated list  of nodes that have the specified attribute.")

mgroup.add_argument('-s',nargs='*',metavar='attr', help="displays a space separated list of nodes that have the specified attribute.")

parser.add_argument('-v', nargs='+', metavar=('node', 'attr'), help="returns any value associated with the attribute and the node.") 

parser.add_argument('-Q', nargs='+', metavar=('node', 'attr'), help="returns 0 to the environment if the conditions are met; 1 otherwise") 

vgroup = parser.add_argument_group("vgroup")
vgroup.add_argument('-V', metavar='attr', help="prints all the values that exist for a specific attribute")

vgroup.add_argument('-U', help="prints out only unique values for a particular attribute", action="store_true")

parser.add_argument('-l', nargs='*', metavar='node', help='prints all the attributes/values associated with the node. if no node is specified, all of the attributes are listed.')

args = parser.parse_args()

def parsequery(results):
        list = []
        for element in results:
                for e in element:
                        if (e != None):
                                list.append(e)
        return list

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

def cluster(nodes):
	clusters = []
	clustered_nodes = []
	current = []
	for node in nodes:
		clust = node[0:len(node)-1]
		if clust in clusters:
			current.append(node)
		else:
			past = current.copy()
			clustered_nodes.append(past)
			clusters.append(clust)
			current.append(node)
	return clustered_nodes

def formatnodes(nodes, attr=None, excludeattr=None): 
	toprint = "";
	clusters = []
	for node in nodes:
		clust = node[0:len(node)-1]	
		if not clust in clusters:
			clusters.append(clust)
			clust += '%'
			if attr == None and excludeattr == None:
				query = ('SELECT node_name FROM NODE WHERE cluster=%s')
				cursor.execute(query, (clust,))
			elif attr != None and excludeattr == None:	
				query = ('SELECT node_name FROM CONFIGURATION  WHERE node_name LIKE %s && gender_name=%s')
				cursor.execute(query, (clust ,attr))
			else:
				query = ('SELECT node_name FROM CONFIGURATION WHERE node_name LIKE %s AND gender_name=%s AND node_name NOT IN (SELECT node_name FROM CONFIGURATION WHERE gender_name=%s)')
				cursor.execute(query, (clust, attr, excludeattr))
			results = parsequery(cursor.fetchall())
			toprint += hostlist.compress_range(results)
			toprint+= ','
	print(toprint[:len(toprint)-1])

def A():
	query = ("SELECT node_name FROM NODE")
	cursor.execute(query)
	results = parsequery(cursor.fetchall())
	return results 

def X(attr, excludeattr): 
	query = ("SELECT node_name FROM CONFIGURATION WHERE gender_name=%s AND node_name NOT IN (SELECT node_name FROM CONFIGURATION WHERE gender_name=%s)")
	cursor.execute(query, (attr, excludeattr))
	results = cursor.fetchall()
	return parsequery(results)

def logic(query):
	if (query[0][0] == '~'):
		attr = query[0][1:len(query[0])]
		query = ('SELECT DISTINCT node_name FROM CONFIGURATION WHERE gender_name!=%s')
		cursor.execute(query, (attr,))
		return parsequery(cursor.fetchall())

if args.q != None:
	excludeattr = None 
	attr = args.q[0]
	if args.A: 
		nodes = A()
	elif args.X != None: 
		nodes = X(attr, args.X)
		excludeattr = args.X
	elif len(args.q) == 3 or attr[0] == '~':
		if (attr[0] == '~'):
			attr = args.q[0][1:len(args.q[0])]
		nodes = logic(args.q) 
	else: 
		nodes= c_n_s_query(attr)
	if len(nodes) != 0:	
		formatnodes(nodes, attr, excludeattr)
elif args.c != None:
	if args.A: 
		results = A()
	elif args.X != None:
		results = X(args.c[0], args.X) 
	else:	
		results = c_n_s_query(args.c[0])
	if (len(results) != 0):
		print(hostlist.delimiter(results, ','))
elif args.n != None:
	if args.A:
		results = A()
	elif args.X != None:
		results = X(args.n[0], args.X)
	else:
		results = c_n_s_query(args.n[0])
	if (len(results) != 0):
		print(hostlist.delimiter(results, '\n'))
elif args.s != None:
	if args.A:
		results = A()
	elif args.X != None:
		results = X(args.s[0], args.X)
	else:
		results = c_n_s_query(args.s[0])
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
		if results[0][0] != None:
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
		if (args.U == True):
			x = np.array(results) 
			results = (np.unique(x)).tolist()
		print(hostlist.delimiter(results, '\n'))
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
