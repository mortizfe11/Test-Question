# routes.py

from test import app
from flask import render_template, request
import sqlite3 as sql

from utils import *

db_name = 'test.db'
db_table = 'test_QA'

init_database(db_name, db_table)

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
        query = f"INSERT INTO {db_table} (question, answer) VALUES ('{question}','{answer}')"
        send_query_within_response(db_name, query)
        title = 'Thanks'
        return render_template('test_createThanks.html', question=question, title=title)
    else:
        return "method no allowed", 405        

@app.route('/question/')
def questions():
    query = f"Select id, question FROM {db_table}"
    questions = send_query_with_response(db_name, query, isAll = True)
    title = 'Questions'
    return render_template('test_questions.html', questions=questions, title=title)

# Display question
@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if request.method == 'GET':
        # send the form
        # add code here to read the question from database
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(db_name, query)
        title = 'Question'
        return render_template('test_question.html', question=question[0], title=title)

    elif request.method == 'POST':
        # read and check answers
        submitted_answer = request.form['answer']

        # code to read the answer from database
        query = f"Select answer FROM {db_table} where id = {id}"
        question = send_query_with_response(db_name, query)
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
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(db_name, query)
        title = 'Edit question'
        return render_template('test_edit.html', id=id, question=question[0], title = title)

    elif request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        query = f"Select question FROM {db_table} where id = {id}"
        question = send_query_with_response(db_name, query)[0]

        query = f"Select question, answer FROM {db_table} where id = {id}"
        old_question, old_answer = send_query_with_response(db_name, query)
        query = f"UPDATE {db_table} SET question='{question}', answer='{answer}' where id = {id}"
        send_query_within_response(db_name, query)    
        title = 'Edit thanks'
        return render_template('test_editThanks.html', 
            id=id, 
            question=question, 
            old_question=old_question,
            title = title
        )

@app.route("/delete/<int:id>", methods=['GET'])
def delete(id):
    query = f"Select question FROM {db_table} where id = {id}"
    question = send_query_with_response(db_name, query)
    
    query = f"DELETE FROM {db_table} WHERE id = {id}"
    send_query_within_response(db_name, query)
    title = 'Delete thanks'
    return render_template('test_deleteThanks.html', question=question[0], title = title)