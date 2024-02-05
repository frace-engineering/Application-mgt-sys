#!/usr/bin/python3
import datetime
from db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response
from flask import abort
#from models import storage

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def this_status():
    return jsonify({"status": "Ok"})

@app.route('/index', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html', time=datetime.datetime.utcnow()) 

@app.route('/index/user', methods=['GET'], strict_slashes=False)
def create_user():
    DB.create_user("10", "Frace", "2 Market road Enugu", "08034721132","friday", "someone@gmail.com",)
    return render_template('index.html', db=DB.show_all())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
