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
			list.append(e)
	return list

mydb = mysql.connector.connect(**config)
cursor = mydb.cursor()

parser.add_argument('-q', metavar='attr', help="Displays a hostrange of nodes that have the specified attribute.")
parser.add_argument('-c', metavar='attr', help="Displays a comma separated list of nodes that have the specified attribute.")
parser.add_argument('-n', metavar='attr', help="Displays a newline separated list  of nodes that have the specified attribute.")
parser.add_argument('-s', metavar='attr', help="Displays a space separated list of nodes that have the specified attribute.")

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
cursor.close()
mydb.close()
