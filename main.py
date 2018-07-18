# The goal of "main.py" is to handle requests of the flask-based server.
# In flask, routes act as a blend of both views & controllers.
#
# n.b. flask uses a WSGI server as the default
#

########################################################
####################### IMPORTS ########################
########################################################

# Flask will provide a robust MVC (model-view-controller) framework for
# standard web dev work. each imported library will be used to build out
# the project
from flask import Flask, redirect, render_template, request, url_for, send_from_directory
# sqlite is the database engine chosen to use
import sqlite3
# need to generate random numbers for the task id
from random import randint

# this is a call to the Flask app constructor, passing "main" as the "name" to
# the newly created app object, so that flask know what files belong to the
# app
app = Flask(__name__)

tasksToDo = [ ] # to be used for maintaining a list of tasks

########################################################
######################## ROUTES ########################
########################################################

# decorator for mapping a GET or POST request for a '/' URL to that of the
# create_task function. in other words, create_task is "registered" to the
# given URL
@app.route('/', methods=["GET", "POST"])
# this route provides access to the task data as visualized by the view
# rendered from the "main.html" file. with the response, the user will be able
# view her tasks along with having the option to create a new task. the html
# utilizes a form for capturing a task's creation.
def create_task():
    global tasksToDo # access project-based list (i.e. 1 per app instance)
    # initiate connection with SQL database    
    connection = sqlite3.connect("project.db")
    # the cursor acts as a pointer to the database
    cursor = connection.cursor()
    
    #### FIRST, handle the GET request
    
    if request.method == "GET": # request.method is a value captured by the
    							# request context imported (generated) from flask. 
    							# it offers, amongst other things, access to the
    							# header data of an http request sent to the flask
    							# server

    	# SQL to access all columns of the database
        selection = """SELECT * FROM main """
        cursor.execute(selection)
        # get all tasks currently stored in the database
        output = cursor.fetchall()
        tasksToDo = []
        # throw them into the global task list
        for task in output:
            tasksToDo.append(task)
        
        # this call will actually render the template for the GET request response,
        # arg1 is the html content to be used for the view, whereas arg2 is the way
        # by which the previously built task list is released to the view. within
        # the html, tasks will be loaded dynamically via the jinja2 templating
        # engine, using the task list global. 
        return render_template('main.html', siteContent = tasksToDo )

    #### SECOND, handle the POST request
    
    else: # a POST request, for this app, constitutes editing of the task list
    
    	# so, random numbers will be used to create a (most probably) unique ID
    	# for each task
        randomID = randint(0,99999)
        # access the form data via request.form
        userName = request.form["userNameOut"] # first input box has name = "userNameOut"
        									   # so that a binding exists for the form
        									   # data passed in the POST
        tasks = request.form["tasks"] # likewise for the second input box, name = "tasks"
        # SQL to insert newly created task into database 
        command =  """INSERT INTO main (taskID, user, tasks)  VALUES ("{i}", "{u}", "{t}");"""
        # format string -> insert form data into "command" string
        outgoingCommand = command.format( i = randomID, u = userName, t = tasks )
        # perform the database migration
        cursor.execute(outgoingCommand)
        # finally, update the database
        connection.commit()
        
        # next, we process the new view for rendering
        # so, use SQL to access new columns (all) of database
        selection = """SELECT * FROM main WHERE user='{x}';"""
        # insert username to "command" string
        formattedSelection = selection.format( x = userName )
        # update pointer to database
        cursor.execute(formattedSelection)
        # get all new tasks stored in the database
        output = cursor.fetchall()
        # update global task list to reflect new tasks
        tasksToDo = []
        for task in output:
            tasksToDo.append(task)
        
        # now, this call will render the template for the POST request response,
        # which is comprised of the newly created tasks. again, like the GET
        # request response, arg1 & arg2 are data passed to the view, which is
        # dynamically rendered via the jinja2 templating engine
        return render_template('main.html', siteContent = tasksToDo ) 

# decorate for mapping the '/remove' URL to that of the remove function. again,
# the function is "registered" to the url
@app.route('/remove/', methods=["GET", "POST"])
# this route provides access to the task data as visualized by the view 
# rendered from the "remove.html" file. with the response, the user will be able
# to not only view her tasks, but also have the ability to remove a task.
# this is handled by inputting the task ID corresponding to the task to be
# removed.
def remove():
    global tasksToDo # access project-based list
    # initiate connection with SQL database
    connection = sqlite3.connect("project.db")
    # the cursor acts as a pointer to the database
    cursor = connection.cursor()
    
    #### FIRST, handle the GET request
    
    if request.method == "GET": # the idea with the GET request is that the user
    							# has not actually removed any data from the task
    							# list, rather she has merely issued a request for
    							# the remove page content only.

        # SQL to access all columns of the database
        selection = """SELECT * FROM main """
        cursor.execute(selection)
        # get all tasks currently stored in the database
        output = cursor.fetchall()
        tasksToDo = []
        # throw them into the global task list
        for task in output:
            tasksToDo.append(task)
        
        # this call to render_template is almost exactly the same as the GET 
        # request processed by the above route for the "main.html" file, except
        # that the user now has the ability to remove a task rather than create
        # a task
        return render_template('remove.html', siteContent = tasksToDo )
    
    #### SECOND, handle the POST request
    
    else: # now, the removal of a task will be handled by a POST request, indicating
    	  # to the app that a captured value, the task ID, via the corresponding 
    	  # form input box 
    	
    	# access the form data via request.form
        removal = request.form["taskRemoval"]
        # SQL command for deleting the task whose task ID is captured
        deleteCommand = """DELETE FROM main WHERE taskID='{d}';"""
        # insert task ID (removal) into "command" string
        formattedSelection = deleteCommand.format( d = removal )
        # perform the database migration
        cursor.execute(formattedSelection)
        # update the database, reflecting the removal of a task
        connection.commit()

        # next, the new page rendering will be created dynamically via the jinja2
        # templating engine to reflect the task removal
        selection = """SELECT * FROM main """
        # update pointer to database
        cursor.execute(selection)
        # get all tasks currently stored in the database
        output = cursor.fetchall()
        tasksToDo = []
        # throw them into the global task list
        for task in output:
            tasksToDo.append(task)
        
        # this call to render_template will render the POST request response for
        # the removal functionality, so the "remove.html" file is passed via arg1.
        # the new tasks to be dynamically updated (again, jinja2 templating), coming
        # from the global tasks list.
    	return render_template('remove.html', siteContent = tasksToDo )
       
# python needs to know whether or not this file is being run as an imported
# module or a script.
if __name__ == '__main__':
   # if it's run as a script, then indicated to flask that the app is to be run
   app.run(debug = False) # a local server will be run