import argparse
import mysql.python.connector
import setP
import loaddata

# Connects to the genders database.
def connectDatabase(password):

    #block tests if gender database exists already
    try:
	try: 
		with open('passW.txt') as f:
			password = [line.rstrip('\n') for line in f][0]
	except Error as e:
		print(e)
		print("Please add your password using --password.")
	config = {
		'user': 'root',
		'password': f'{password}',
		'host': 'localhost',
		'database': 'gender'
	}
        mydb = mysql.connector.connect(**config) 
        if mydb.is_connected():
            cursor = mydb.cursor(buffered=True,dictionary=True)
    #if it does not exists runs create.sql script
    except Error as e:
        print(e)
	config = {
		'user': 'root',
		'password': f'{password}',
		'host': 'localhost'
	}
        mydb = mysql.connector.connect(**config)
        cursor = mydb.cursor(buffered=True , dictionary=True)
        # Open and read the file as a single buffer
        fd = open('create.sql', 'r')
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
	mydb = connectDatabase()
	parser = argparse.ArgumentParser(description='Connect with database')
	parser.add_argument('--password', action='store_true')
	
	parser.add_argument('--load', action="store_true")


	args = parser.parse_args()
	if args.password:
            setP.store() 
	elif args.load:
	    loaddata.main(mydb)


if __name__ == "__main__":
    main()

