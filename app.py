from flask import Flask,render_template	
import redis
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/')
def home():
		return render_template("index.html")

# @app.route('/redis')
# def redis():
# 	r = redis.Redis(host='redis',port='6379',db=0)
# 	try:
# 		if r.ping():
# 			r.incr('compteur')
# 			compteur = r.get('compteur')	
# 			return {
# 			'redis': ['compteur:', str(compteur)]
# 			}
# 	except:
# 		return {
# 			'redis': ['fail']
# 		}

import datetime		
@app.route('/mongo')
def mongo():
    client = MongoClient('localhost', 27017)
    db = client.test_database
    collection = db.test_collection
    print(collection)
    post = {"author": "Mike",
    "text": "My first blog post!",
    "tags": ["mongodb", "python", "pymongo"],
    "date": datetime.datetime.utcnow()}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print(post_id)


# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)