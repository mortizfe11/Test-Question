# routes.py

from test import app
from flask import render_template, request
import sqlite3 as sql

db_name = 'test.db'
db_table = 'test_QA'
# connect to qa_database.sq (database will be created, if not exist)
con = sql.connect(db_name)
con.execute(f'CREATE TABLE IF NOT EXISTS {db_table} (ID INTEGER PRIMARY KEY AUTOINCREMENT,'
            + 'question TEXT, answer TEXT)')
con.close()

def send_query_within_response(query):
    try:
        con = sql.connect(db_name)    
        c =  con.cursor() # cursor
        # insert data
        c.execute(query)  
        con.commit() # apply changes
    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return render_template('test_database_error.html', error=err)
    finally:
        con.close() # close the connection

def send_query_with_response(query, isAll = False):
    try:
        con = sql.connect(db_name)    
        c =  con.cursor() # cursor
        # insert data
        c.execute(query)  
        if isAll:
            question = c.fetchall()
        else:
            question = c.fetchone()
        con.commit() # apply changes
        return question

    except con.Error as err: # if error
            # then display the error in 'database_error.html' page
        return render_template('test_database_error.html', error=err)
    finally:
        con.close() # close the connection

# home page
@app.route('/')  # root : main page
def index():
    # by default, 'render_template' looks inside the folder 'template'
    return render_template('test_index.html')

# Create question
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        # send the form
        return render_template('test_create.html')

    elif request.method == 'POST':
        # read data from the form and save in variable
        question = request.form['question']
        answer = request.form['answer']

        # store in database
        # add code here
        query = f"INSERT INTO {db_table} (question, answer) VALUES ('{question}','{answer}')"
        send_query_within_response(query)
        return render_template('test_createThanks.html', question=question)
    else:
        return "method no allowed", 405        

@app.route('/question/')
def questions():
    query = f"Select id, question FROM {db_table}"
    questions = send_query_with_response(query, isAll = True)
    return render_template('test_questions.html', questions=questions)

# Display question
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if request.method == 'GET':
        # send the form
        # add code here to read the question from database
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(query)
        return render_template('test_question.html', question=question[0])

    elif request.method == 'POST':
        # read and check answers
        submitted_answer = request.form['answer']

        # code to read the answer from database
        query = f"Select answer FROM {db_table} where id = {id}"
        question = send_query_with_response(query)
        correct_answer = question[0]

        if submitted_answer == correct_answer:
            return render_template('test_correct.html')
        else:
            return render_template('test_sorry.html',
                answer = correct_answer,
                yourAnswer = submitted_answer
            )

    else:
        return "method no allowed", 405

@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(query)
        return render_template('test_edit.html', id=id, question=question[0])

    elif request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(query)[0]

        query = f"Select question, answer FROM {db_table} where id = {id}"
        old_question, old_answer = send_query_with_response(query)
        query = f"UPDATE {db_table} SET question='{question}', answer='{answer}' where id = {id}"
        send_query_within_response(query)    
        return render_template('test_editThanks.html', id=id, question=question, old_question=old_question)

@app.route("/delete/<int:id>", methods=['GET'])
def delete(id):

    query = f"Select question FROM {db_table} where id = {id}"
    question = send_query_with_response(query)
    
    query = f"DELETE FROM {db_table} WHERE id = {id}"
    send_query_within_response(query)
    return render_template('test_deleteThanks.html', question=question[0])