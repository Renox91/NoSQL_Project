# Imports flask
from flask import Flask, session, render_template, request, redirect, url_for
from flask.helpers import flash 

# Imports database
import redis
import psycopg2
from pymongo import MongoClient

# Others imports
import bcrypt
from datetime import date, timedelta
import sys

# App
app = Flask(__name__)

# MongoDB
client = MongoClient('mongodb',27017)
db = client.userdb

# Redis
redisdb = redis.Redis(host = 'redis', port = 6379)

#Postgres
postgresdb = psycopg2.connect(
  host="postgres",
  user="test",
  password="test",
  database="test"
)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html')

    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    users = db.userdb
    login_user = users.find_one({'username': request.form['username']})
    
    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            if request.form.get('remember'):
                session.permanent = True
            else:
                session.permanent = False
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    flash("Bad Username or Password", "warning")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        users = db.userdb
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'username' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        flash("That username already exists!")
        return redirect(url_for('register'))

    return render_template('register.html')
    
@app.route('/scores')
def scores():
    if 'username' in session:
        # db_items = db.userdb.find()
        # items = [item for item in db_items]
        # return render_template('scores.html', items = items)

        cursordb = postgresdb.cursor()
        cursordb.execute("Select * from scores")
        keys = cursordb.fetchall()
        # data_keys = []
        # data_values = []
        # # keys = redisdb.keys('*')
        # for key in keys:
        #     data_keys.append(key[2])
        #     data_values.append(key[3])

        return render_template('scores.html', data = keys)
    return redirect(url_for('index'))
    
@app.route('/add_score', methods = ['POST'])
def add_score():
    cursordb = postgresdb.cursor()
    cursordb.execute("""INSERT INTO scores(
	game, username, score, date_score)
	VALUES (%s, %s, %s, %s)""",(request.form['game'],session['username'],request.form['score'],date.today()))
    postgresdb.commit()

    # redisdb.set(session['username'], request.form['score'])
    return redirect(url_for('scores'))

@app.route('/casse_brique', methods =['GET'])
def casse_brique():
    if 'username' in session:
        return render_template('casse_brique.html')

    return redirect(url_for('index'))

@app.route('/pong', methods =['GET'])
def pong():
    if 'username' in session:
        return render_template('pong.html')

    return redirect(url_for('index'))

@app.route('/redisdbs')
def redisdbs():
    redisdb.incr('hits')
    return f"index: {redisdb.get('hits')}"

@app.route('/stats')
def stats():
    if 'username' in session:
        cursordb = postgresdb.cursor()
        cursordb.execute(f"select * from scores where username = '{session['username']}'")
        data = cursordb.fetchall()
        return render_template('stats.html',data = data)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = '65416546zzefuihs45684d6zf'
    app.permanent_session_lifetime = timedelta(days = 5)
    app.run(host='0.0.0.0', port=80, debug=True)