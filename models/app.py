#!/usr/bin/python3
import datetime
from service_provider import Provider
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

@app.route('/index/provider', methods=['GET'], strict_slashes=False)
def create_provider():
    DB.create_provider(10, "Frace", "2 Market road Enugu", "08034721132","friday", "one@gmail.com",)
    return render_template('index.html', db=DB.show_all)

@app.route('/index/service', methods=['GET'], strict_slashes=False)
def create_service():
    DB.create_service(10, "IT Services", "Debugging your system")
    return render_template('index.html', db=DB.show_all)

@app.route('/index/client', methods=['GET'], strict_slashes=False)
def create_client():
    DB.create_client(1, "Gitfarrah", "Chukwu", "Gift", "08034721132","friday", "one@gmail.com",)
    return render_template('index.html', db=DB.show_all)

@app.route('/index/appointment', methods=['GET'], strict_slashes=False)
def create_appointment():
    DB.create_appointment(10, "Frace", datetime.datetime.utcnow())
    return render_template('index.html', db=DB.show_all)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
