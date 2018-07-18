# The goal of "test.py" is to enact a basic first pass test to the app's database
#

# sqlite is the database engine chosen to use
import sqlite3

# initiate connection with SQL database
connection = sqlite3.connect("project.db")
# here, the cursor acts as a pointer to the database
cursor = connection.cursor()

# SQL command, as updated via the database cursor, will get all columns for whom
# the user is "humphrey"
cursor.execute("""SELECT * FROM main WHERE user='humphrey';""") 
# grab all such available data for said user
result = cursor.fetchall() 
# throw it into a string & print the contents to standard output
for r in result:
    print(str(r))