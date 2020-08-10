#!/usr/bin/python
import io
from shutil import copyfile
import subprocess
from pathlib import Path
import os;
import genders;
import mysql.connector 
from mysql.connector import Error
import argparse;

#sets up connection to genders database
def connectDatabase():

	#block tests if gender database exists already
    try:

	#connection set up using a password I created to run mysql on boron2
	#I think I want to look into making that passwordless since this would
	#only work on boron2

        mydb = mysql.connector.connect( host="localhost",user="root",password="Puffyf15", database="gender")
	
        if mydb.is_connected():
            print('Connected to MySQL database')
            cursor = mydb.cursor(buffered=True,dictionary=True)

	#if it does not exists runs createAll.sql script 
    except Error as e: 
        print(e)
        mydb = mysql.connector.connect( host="localhost", user="root", password="Puffyf15" )
        cursor = mydb.cursor(buffered=True , dictionary=True)
		# Open and read the file as a single buffer
        fd = open('createALL.sql', 'r')
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split(';')
		# Execute every command from the input file
        for command in sqlCommands:
   		# This will skip and report errors
            try:
                cursor.execute(command)
            except Error as e:
                print ("Command skipped: ", e)
    return mydb

#looks through given genders file and parses node information.
#if gender already exists on the node it does not insert
def parse_file(filename,mydb):
    gens = genders.Genders(filename)
    all = gens.getattr_all()
    nod = gens.getnodes()
    for y in nod:
        insertNode(y,mydb)
    for x in all:
        insertGender(x,mydb)
        spnod = gens.getnodes(attr=x)
        for k in spnod:
             insertConfig(gens.getattrval(attr=x,node=k),k,x,mydb)

#debugging function. prints all nodes and genders on nodes
def print_all(mydb):
    sel = "SELECT * FROM CONFIGURATION"
    cur = mydb.cursor()
    cur.execute(sel)
    records = cur.fetchall()
    for row in records:
        print(row)


def insertNode(node_name,mydb):
    cluster = node_name[:-1]
    node_num = node_name[-1:]
    sql = "INSERT IGNORE INTO NODE (cluster, node_num, node_name) VALUES (%s, %s, %s)"
    val = (cluster, node_num, node_name)
    cursor = mydb.cursor(buffered=True , dictionary=True)
    try:
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.ProgrammingError as err:
        print(err.errno)
   # print("inserting")

def insertGender(gender_name,mydb):
    sql = "INSERT IGNORE INTO GENDER(gender_name,descrip) VALUES (%s,%s)"
    val = (gender_name,'none')
    cur = mydb.cursor(buffered=True, dictionary=True)
    try:
        cur.execute(sql,val)
        mydb.commit()
    except mysql.connector.ProgrammingError as err:
        print(err.errno)

def insertConfig(val, node_name, gender_name, mydb):
    config_id = node_name + gender_name
    sql = "INSERT IGNORE INTO CONFIGURATION(config_id,val,node_name,gender_name) VALUES (%s,%s,%s,%s)"
    val = (config_id,val,node_name,gender_name)
    cur = mydb.cursor(buffered=True, dictionary=True)
    try:
        cur.execute(sql,val)
        mydb.commit()
    except mysql.connector.ProgrammingError as err:
        print(err.errno)

#show all genders in database
def allGenders(mydb):
    sql = "SELECT DISTINCT gender_name FROM GENDER"
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql)
    records = cur.fetchall()
    print("All genders in database: \n")
    for row in records:
        print(row['gender_name'])

#all nodes that have particular gender
def findNodes(mydb,gender_namei):
    sql = "SELECT DISTINCT n.node_name FROM NODE n JOIN CONFIGURATION c WHERE (n.node_name = c.node_name AND c.gender_name = %s )"
    val = (gender_namei,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    records = cur.fetchall()
    print("Nodes containing gender: ",gender_namei)
    for row in records:
        print(row['node_name'])

#all genders in a particular node
def findGenders(mydb,node_namei):
    sql = "SELECT DISTINCT g.gender_name FROM GENDER g JOIN CONFIGURATION c WHERE (g.gender_name = c.gender_name AND c.node_name = %s)"
    val = (node_namei,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    records = cur.fetchall()
    print("All genders of the node: ",node_namei)
    for row in records:
        print(row['gender_name'])

#opens file containing paths to genders file in cluster
#copies each file into temp file and sends that to be parsed into database
def parse_pathfi(filename,mydb):
    
    with open(filename) as f:
        mylist = [line.rstrip('\n') for line in f]

        for y in mylist:
            dest = "tempfile.txt"
            copyfile(y, dest)
            parse_file(dest,mydb)
    

def main():
    mydb = connectDatabase()
    #insertNode("practice1",mydb)
    #insertGender("pretend_name","description",mydb)
   # insertConfig("val", "practice1", "pretend_name", mydb) 
    #parse_file("gentestfi.txt",mydb)
    print_all(mydb)
   # allGenders(mydb)
   # findNodes(mydb,"center")
   # findGenders(mydb,"lgw1")
   # ex1 = open("pypath.sh")
   # subprocess.call(ex1,shell=True)
   # ex2 = open("libpath.sh",shell=True)
   # subprocess.call(ex2,shell=True)
    fi = open("get_genders_file.sh")
    subprocess.call(fi,shell=True)
    fi.close()    
    parse_pathfi("pathfile.txt",mydb)
   # print_all(mydb)
#execute qureies 
if __name__ == "__main__":
    main()
