# The goal of "Database Creation.py" is self-explanatory, namely to create the
# database for the app.
#

# sqlite is the database engine chosen to use
import sqlite3

# initiate connection with SQL database
connection = sqlite3.connect("project.db")
# whereas, the cursor acts as a pointer to the database
cursor = connection.cursor()

# this "command" string is the SQL for creating the "main" table of the database.
# in fact, it is the only such table, for the app economically employs a single table
# for the model. the table is comprised of 3 columns:
#	(1) taskID - a variable length unicode type used to represent the (probably) 
#				unique ID for a given task,
#	(2) user - a variable length unicode type used to represent the user,
#	(3) tasks - a variable length unicode type use to represent the task data (i.e.
#				a string that acts as the content of a given task)
sql_command = """
CREATE TABLE main (
taskID VARCHAR,
user VARCHAR, 
tasks VARCHAR 
);"""

# update the database
cursor.execute(sql_command)