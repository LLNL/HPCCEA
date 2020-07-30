#!/usr/bin/python3

import argparse
parser = argparse.ArgumentParser("genders database query")

import genders 
gen = genders.Genders(filename="/etc/genders")

import mysql.connector

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
			list.append(e)
	return list

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

# getattr(self, node): returns a list of attributes for the speicified node; if empty, use the current node 
parser.add_argument('--getattr', nargs='?', const="", help="Returns a list of attributes for the specified node. If the node is not specified, the local node's attributes are returned.")
parser.add_argument('--getattrval', nargs='*', default=[None, None], metavar=('attribute', 'node'), type=str, help="Input an attribute, and then a node to get the value") 

args = parser.parse_args()

if args.getattr != None:
	node = args.getattr
	if (len(args.getattr) == 0): #Default option, use current node
		node = gen.getnodename()
	query = ("SELECT gender_name FROM CONFIGURATION WHERE node_name=%s")
	cursor.execute(query, (node,))
	results = cursor.fetchall()
	if len(results) == 0:
		parser.error("That node name does not exist.")
	else:
		print(parsequery(results))
elif args.getattrval != None:
	attribute = ""
	node = ""
	if len(args.getattrval) == 0:
		parser.error("Need to specify attribute")
	elif len(args.getattrval) == 1:
		attribute = args.getattrval[0]
		node = gen.getnodename()
	else:
		attribute = args.getattrval[0]
		node = args.getattrval[1]
	print("Got defaults or arguments")
	print("Gender: " + attribute) 
	print("Node: " + node)

cursor.close()
mydb.close()
