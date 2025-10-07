from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_cors import CORS

from flask_caching import Cache
import redis

from celery_config import celery


app = Flask(__name__)
CORS(app, origins='*')

# app.secret_key='12341234'
redis_client = redis.Redis(host="localhost", port=6380, db=0)
cache = Cache(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS': redis_client})


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatalbm.sqlite3"
app.config['JWT_SECRET_KEY'] = '123456'
celery.conf.update(app.config)


from routes import *


        



if __name__ == '__main__':
    app.run(debug=True,)