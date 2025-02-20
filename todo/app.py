from flask import Flask, render_template, request, redirect
from datetime import datetime
import pytz

app = Flask(__name__)

TODOS = []


@app.route("/")
def index():
    return render_template("index.html", num_tasks=len(TODOS))

@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        # get the current date for the form
        today = datetime.now(pytz.timezone("America/Indianapolis"))
        # show a form for the user to add a new task
        return render_template("add.html", today=today.strftime("%Y-%m-%d"))
    else: # the user submitted the form
        # get the data from the form
        task = request.form.get("task", "")
        task_date = request.form.get("task-date", "")
        task_priority = request.form.get("task-priority", "normal")
        # validation
        if task == "":
            msg = "Please enter a valid task."
            return render_template("error.html", error_msg=msg)
        elif task_date == "":
            msg = "Invalid date for this task"
            return render_template("error.html", error_msg=msg)
        elif task_priority == "":
            msg = "No priority was selected"
            return render_template("error.html", error_msg=msg)
        else:
            # now add the task to the TODOS list
            # create a python dictionary (dict)
            todo = {
                "name": task,
                "date": task_date,
                "priority": task_priority
            }
            # add the dict to the list of TODOS
            TODOS.append(todo)

            return redirect("/show")

@app.route("/show")
def show():
    # show a list of all the TODOS
    task_list = TODOS
    return render_template("show.html", task_list=task_list)


@app.route("/delete/<int:index>")
def delete_task(index):
    # check to see if there is a task at that index
    if index >= len(TODOS):
        msg = "NO TASK FOUND!!! :( "
        return render_template("error.html", error_msg=msg)
    else:
        task = TODOS[index]
        # usualy when you delete, you would get confirmation from the user
        TODOS.pop(index) # take the task out of the TODOS list
        return render_template("delete.html", task=task)

@app.route("/edit/<int:index>")
def edit(index):
    if index >= len(TODOS):
        msg = "NO TASK FOUND!!! :( "
        return render_template("error.html", error_msg=msg)
    task = TODOS[index]
    return render_template("add.html", task=task, today=task["date"])






