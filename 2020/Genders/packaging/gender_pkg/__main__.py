import argparse
import mysql-python
import setP

# Connects to the genders database. 
def connectDatabase(password):
    #block tests if gender database exists already
    try:
	config = {
	  'user': 'root'
	  'password': '%s'
# Command in main to write to file with password  


        mydb = mysql.connector.connect( host="localhost",user="root",password="Puffyf15", database="gender")
        if mydb.is_connected():
            cursor = mydb.cursor(buffered=True,dictionary=True)
    #if it does not exists runs create.sql script
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

def main():
	# Find a way to enable passwordless OR store the password after the first command for a certain period of time 
	parser = argparse.ArgumentParser(description='Connect with database')
	parser.add_argument('password', type=str)
	


	args = parser.parse_args()
	

	if args.password != None:
            setP.store()  


if __name__ == "__main__":
    main()

