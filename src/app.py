from flask import Flask, session, render_template, request, redirect, url_for 
import redis
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb',27017)
db = client.userdb

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=["POST"])
def login():
    users = db.userdb
    login_user = users.find_one({'username': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Mauvais username/password'

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
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/redis')
def redis():
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    r.get('foo')

@app.route('/mongo')
def mongo():
    db_items = db.userdb.find()
    items = [item for item in db_items]

    return render_template('scores.html', items = items)

@app.route('/add_score', methods = ['POST'])
def add_score():
    item_doc = {
        'pseudo': request.form['pseudo'],
        'score': request.form['score']
    }
    db.userdb.insert_one(item_doc)
    return redirect(url_for('mongo'))

@app.route('/casse_brique', methods =['GET'])
def casse_brique():
    return render_template('casse_brique.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(host='0.0.0.0', port=80, debug=True)