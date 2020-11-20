from flask import Flask, render_template, request, redirect, url_for 
import redis
from pymongo import MongoClient
from app import app, db
import bcrypt

@app.route('/login', methods=["POST"])
def login():
    users = db.userdb
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Mauvais username/password'

@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        users = db.userdb
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')