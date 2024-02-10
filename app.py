#!/usr/bin/python3
import datetime
from models.db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response, request, url_for
from models.base_models import Provider, Appointment, Service, Client
from flask import abort

app = Flask(__name__)
app.config['SECRETE_KEY'] = '16b0c77ece0958b3a5914bc951c1961e106ecbb511141f10515dee07b5e4453113c9'


@app.route('/', methods=['GET'], strict_slashes=False)
def this_status():
    return jsonify({"status": "Ok"})

@app.route('/appoms', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/appoms/signup', methods=['GET'], strict_slashes=False)
def sign_up():
    return render_template('sign_up.html') 

@app.route('/appoms/contacts', methods=['GET'], strict_slashes=False)
def contacts():
    return render_template('contacts.html') 

@app.route('/appoms/about', methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/appoms/services', methods=['GET'], strict_slashes=False)
def services():
    return render_template('services.html')

@app.route('/appoms/providers', methods=['GET'], strict_slashes=False)
def providers():
    return render_template('providers.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
