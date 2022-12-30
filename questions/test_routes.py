# routes.py

#from sqlite3 import Error
from test import app

from pymysql import Error
from flask import render_template, request

from utils_mysql import *

db_name = 'test.db'
db_table = 'test_QA'

create_table_if_not_exist(db_name, db_table)

# Si detectó un error, visualizará la vista del error.
def is_view_error(err):
    if err == Error: 
        title = 'Database'
        return render_template('test_database_error.html', error=err, title=title)

# Petición al select de la BDD
def ask_select(db_name, db_table, name_cols, id = 0):
    question = select(db_name, db_table, name_cols, id)
    is_view_error(question) 
    return question

# Petición al delete de la BDD
def ask_delete(db_name, db_table, id):
    flag = delete(db_name,db_table,id)
    print(flag)
    is_view_error(flag)

# Petición al insert de la BDD
def ask_insert(db_name, db_table, values):
    flag = insert(db_name,db_table, values)
    is_view_error(flag)

# Petición al update de la BDD
def ask_update(db_name, db_table, values, id):
    flag = update(db_name,db_table, values, id)
    is_view_error(flag)

# home page
@app.route('/')  # root : main page
def index():
    # by default, 'render_template' looks inside the folder 'template'
    title = "Home"
    return render_template('test_index.html', title=title)

# Create question
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # send the form
        title = 'Create'
        return render_template('test_create.html', title=title)

    elif request.method == 'POST':
        # read data from the form and save in variable
        question = request.form['question']
        answer = request.form['answer']

        # store in database
        # add code here
        ask_insert(db_name, db_table, [question, answer])
        title = 'Thanks'
        return render_template('test_createThanks.html', question=question, title=title)
    else:
        return "method no allowed", 405        

@app.route('/question/')
def questions():
    name_cols = ['id', 'question']
    questions = ask_select(db_name, db_table, name_cols)
    title = 'Questions'
    return render_template('test_questions.html', questions=questions, title=title)

# Display question
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if request.method == 'GET':
        # send the form
        # add code here to read the question from database
        name_cols = ['question']
        question = ask_select(db_name, db_table, name_cols, id)
        title = 'Question'
        return render_template('test_question.html', question=question[0], title=title)

    elif request.method == 'POST':
        # read and check answers
        submitted_answer = request.form['answer']

        # code to read the answer from database

        name_cols = ['answer']
        question = ask_select(db_name, db_table, name_cols, id)
        correct_answer = question[0]

        if submitted_answer == correct_answer:
            title = 'Congratulation'
            return render_template('test_correct.html', title = title)
        else:
            title = 'Sorry'
            return render_template('test_sorry.html',
                answer = correct_answer,
                yourAnswer = submitted_answer,
                title = title
            )

    else:
        return "method no allowed", 405

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':

        name_cols = ['question']
        question = ask_select(db_name, db_table, name_cols, id)
        title = 'Edit question'
        return render_template('test_edit.html', id=id, question=question[0], title = title)

    elif request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']

        values = [question, answer]
        #name_cols = ['question']
        #question = ask_select(db_name, db_table, name_cols, id)[0]

        name_cols = ['question', 'answer']
        old_question, old_answer = ask_select(db_name, db_table, name_cols, id)

        ask_update(db_name, db_table, values, id)
        
        title = 'Edit thanks'
        return render_template('test_editThanks.html', 
            id=id, 
            question=question, 
            old_question=old_question,
            title = title
        )

@app.route("/delete/<int:id>", methods=['GET'])
def delete(id):
    name_cols = ['question']
    question = ask_select(db_name, db_table, name_cols, id)
    print(id, question)
    ask_delete(db_name, db_table, id)
    title = 'Delete thanks'
    return render_template('test_deleteThanks.html', question=question[0], title = title)