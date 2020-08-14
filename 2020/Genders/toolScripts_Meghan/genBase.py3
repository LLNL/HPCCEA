#!/usr/bin/python
import hostlist
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
         #   print('Connected to MySQL database')
            cursor = mydb.cursor(buffered=True,dictionary=True)

	#if it does not exists runs createAll.sql script 
    except Error as e: 
        print(e)
        mydb = mysql.connector.connect( host="localhost", user="root", password="" )#put your pasword here
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
    records = allNodes(mydb)    
    flag = False
    for y in nod:
        insertNode(y,mydb)
    conIDs = []
    for x in all:
        insertGender(x,mydb)
        spnod = gens.getnodes(attr=x)
        for k in spnod:
             insertConfig(gens.getattrval(attr=x,node=k),k,x,mydb)
             conIDs.append(k+x)
    return nod,all,conIDs
#debugging function. prints all nodes and genders on nodes
def print_all(mydb):
    sel = "SELECT * FROM CONFIGURATION"
    cur = mydb.cursor()
    cur.execute(sel)
    records = cur.fetchall()
    for row in records:
        print(row)

def checkE(node_name,mydb):
    sql = "EXISTS (SELECT DISTINCT node_name FROM GENDER WHERE node_name = %s)"
    val = (node_name,)
    cursor = mydb.cursor(buffered=True , dictionary=True)
    cursor.execute(sql,val)
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

def deleteNode(node_name,mydb):
    sql = "DELETE FROM NODE WHERE node_name = %s"
    val = (node_name,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    mydb.commit()


def insertGender(gender_name,mydb):
    sql = "INSERT IGNORE INTO GENDER(gender_name,descrip) VALUES (%s,%s)"
    val = (gender_name,'none')
    cur = mydb.cursor(buffered=True, dictionary=True)
    try:
        cur.execute(sql,val)
        mydb.commit()
    except mysql.connector.ProgrammingError as err:
        print(err.errno)

def deleteGender(gender_name,mydb):
    sql = "DELETE FROM GENDER WHERE gender_name = %s"
    val = (gender_name,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    mydb.commit()


def insertConfig(val, node_name, gender_name, mydb):
    #check if exists if yes, compare vals if dif update
    #print("inserting config")
    config_id = node_name + gender_name
    sql = "INSERT IGNORE INTO CONFIGURATION(config_id,val,node_name,gender_name) VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE val = %s"
    val = (config_id,val,node_name,gender_name,val)
    cur = mydb.cursor(buffered=True, dictionary=True)
    try:
        cur.execute(sql,val)
        mydb.commit()
    except mysql.connector.ProgrammingError as err:
        print(err.errno)

def deleteConfig(config_idi,mydb):
    sql = "DELETE FROM CONFIGURATION WHERE config_id = %s"
    val = (config_idi,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    mydb.commit()

#return list of all confis
def allConfigs(mydb):
    sql = "SELECT DISTINCT config_id FROM CONFIGURATION"
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql)
    records = cur.fetchall()
    return records 
#show all genders in database
def allGenders(mydb):
    #print("inall")
    sql = "SELECT DISTINCT gender_name FROM GENDER"
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql)
    records = cur.fetchall()
    #print("All genders in database: \n")
    #for row in records:
    #    print(row['gender_name'])
    return records
#Pulls all of the nodes in database
def allNodes(mydb):
#    print("why")
    sql = "SELECT DISTINCT node_name FROM NODE"
    cur = mydb.cursor(buffered=True,dictionary=True)
    cur.execute(sql)
    records = cur.fetchall()
    #return records
  #  for row in records:
   #     print("from all node query",row['node_name'])
    return records
def getVals(mydb,gender_name):
    gender_name = str(gender_name)
    sql = "SELECT val,node_name FROM CONFIGURATION WHERE gender_name = %s"
    cur = mydb.cursor(buffered=True,dictionary=True)
    val = (gender_name,)
    #print(gender_name)
    cur.execute(sql,val)
    records = cur.fetchall()
    return records    

#all nodes that have particular gender
def findNodes(mydb,gender_namei):
    sql = "SELECT DISTINCT n.node_name FROM NODE n JOIN CONFIGURATION c WHERE (n.node_name = c.node_name AND c.gender_name = %s )"
    val = (gender_namei,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    records = cur.fetchall()
   # print("Nodes containing gender: ",gender_namei)
    
   # for row in records:i
   #     print(row['node_name'])
    return records

def findGenders(mydb,node_namei):
    sql = "SELECT DISTINCT g.gender_name FROM GENDER g JOIN CONFIGURATION c WHERE (g.gender_name = c.gender_name AND c.node_name = %s)"
    val = (node_namei,)
    cur = mydb.cursor(buffered=True, dictionary=True)
    cur.execute(sql,val)
    records = cur.fetchall()
   # print("All genders of the node: ",node_namei)
    for row in records:
        print(row['gender_name'])

#all genders in database
 
#opens file containing paths to genders file in cluster
#copies each file into temp file and sends that to be parsed into database
def parse_pathfi(filename,mydb):
    fileNode = []
    adjLi = []
    genderFile = []
    configs = []
    with open(filename) as f:
        mylist = [line.rstrip('\n') for line in f]

        for y in mylist:
            dest = "tempfile.txt"
            copyfile(y, dest)
            nod,all,conf = parse_file(dest,mydb)
            fileNode.append(nod)
            genderFile.append(all)
            configs.append(conf)
    cid = []
    for c in configs:
        for cc in c:
            cid.append(cc)
    #for id in cid:
    #    print(id)

    fileGender = []
    for x in genderFile:
        for n in x:
            fileGender.append(n)
      
    for n in fileNode:
        for jj in n:
            adjLi.append(jj)
    
    idRec = allConfigs(mydb)
    idDel = []
    for rec in idRec:
        idDel.append(rec['config_id'])

#    idDel = []

    for ll in idRec:
        for lll in cid:
            if ll['config_id'] == lll:
                if lll in idDel: idDel.remove(lll)
    for rem in idDel:
        #print("deleting ",rem)
        deleteConfig(rem,mydb)
        
    genRecords = allGenders(mydb)
    genDel = []
    for g in genRecords:
         genDel.append(g['gender_name'])
    records = allNodes(mydb)
    realLi = []
    
    for k in genRecords:
        for f in fileGender:
            #print("f is ",f)
            if k['gender_name'] == f:
                #print("removing gender ",f)
                if f in genDel: genDel.remove(f)
    for r in records:
        realLi.append(r['node_name'])
    
    for rec in records:
        for u in adjLi:
            if rec['node_name'] == u:
               #  print("removing ",u)
                 realLi.remove(u)
   
    for det in realLi:
        deleteNode(det,mydb)

    for tt in genDel:
        deleteGender(tt,mydb)
    #    for y in nod:
    #        if y == rec['node_name']:
    #            there = True
    #            nod.remove(y)
    #print(len(nod))
    #for det in nod:
    #    print("deleting node", det)
    #    deleteNode(det,mydb)

def main():
    mydb = connectDatabase()
    #insertNode("practice1",mydb)
    #insertGender("pretend_name","description",mydb)
   # insertConfig("val", "practice1", "pretend_name", mydb) 
    #parse_file("gentestfi.txt",mydb)
    #print_all(mydb)
   # allGenders(mydb)
   # findNodes(mydb,"center")
   # findGenders(mydb,"lgw1")
   # ex1 = open("pypath.sh")
   # subprocess.call(ex1,shell=True)
   # ex2 = open("libpath.sh",shell=True)
   # subprocess.call(ex2,shell=True)

#adding command arguments
    parser = argparse.ArgumentParser(description='Gender quereies from central database.')
    parser.add_argument('--comb',help='pulls genders file from cfengine and inserts into database',action='store_true',dest='comb')

    parser.add_argument('-dd',help='drops entire database',action='store_true',dest='dd')

    parser.add_argument('-q', nargs=1,help='prints list of nodes having the specified attribute in host range',action='store', dest='hostNode')
  
    parser.add_argument('-c',nargs=1,help='prints list of nodes having specified attribute in coma seperated format',action='store',dest='comaNode')
    #results = parser.parse_args()

    parser.add_argument('-n',nargs=1,help='prints list of nodes having specified attribute in newline separated list',action='store',dest='newNode')

    parser.add_argument('-s',nargs=1,help='prints list of nodes having specified attribute in space separated list',action='store',dest='spaceNode')

    parser.add_argument('-v',nargs=1,help='outputs values associated with gender',action='store',dest='vals')

    parser.add_argument('-vv',nargs=1,help='outputs values associated with gender and with node listed',action='store',dest='valv')

    parser.add_argument('-l',nargs='*',help='list of attributes for a particular node, if no node all attributes in database')

    
    results = parser.parse_args()

#run based on input

#pull files from cfengine 
    if results.comb:
        fi = open("get_genders_file.sh")
        #subprocess.call(fi,shell=True)
        os.system("ls -d ~/cfengine/clusters/*/genders > pathfile.txt")
        fi.close()
        parse_pathfi("pathfile.txt",mydb)

    if results.dd:
        sql = "DROP DATABASE gender"
        cur = mydb.cursor(buffered=True, dictionary=True)
        cur.execute(sql)
#finds nodes w specified gender in hostlist format
    if results.hostNode != None:
        finLi = []
        prev = False
        hosts = ''
        clusterN = ""
        records = findNodes(mydb,str(results.hostNode[0]))
        cluster0 = records[0]
        cluster0 = cluster0['node_name']
        cluster0 = cluster0[:-1]

        for row in records:
            clusterT = row['node_name']
            clusterT = clusterT[:-1]
           # print("debug: ",clusterT)
            if cluster0 == clusterT:
                hosts += ( row['node_name'] + ',')
                prev = True
            elif cluster0 != clusterT and prev == True:                
                finLi.append(hosts)
                hosts = ''
                hosts += ( row['node_name'] + ',')
                prev = False
            elif cluster0 != clusterT and prev == False:
                hosts = ''
                hosts += ( row['node_name'] + ',')
                prev = True
            cluster0 = clusterT
        finLi.append(hosts)
        for y in finLi:
            y = y[:-1] 
            y = hostlist.compress_range(y)
            print(y, end=" ")
    if results.comaNode != None:
        finLi = []
        records = findNodes(mydb,str(results.comaNode[0]))
         
        for row in records:
            finLi.append(row['node_name'])
    
        print(*finLi,sep=", ")
    if results.newNode != None:
        records = findNodes(mydb,str(results.newNode[0]))
        
        for row in records:
            print(row['node_name'])
    if results.spaceNode != None:
       records = findNodes(mydb,str(results.spaceNode[0]))
       
       for row in records:
           print(row['node_name'],end=" ")

    if results.vals != None:
        records = getVals(mydb,*results.vals)
        for row in records:
            print(row['val'])
    
    if results.valv != None:
        records = getVals(mydb,*results.valv)
        for row in records:
            print(row['node_name']," ",row['val'])

    if results.l != None:
        #print("debug1")
        if len(results.l) > 0:
            #print(results.l)
            findGenders(mydb,*results.l)
        else:
         #   print("here")
            records = allGenders(mydb)
            for row in records:
                print(row['gender_name'])

if __name__ == "__main__":
    main()
