#!/usr/bin/python3
import datetime
from models.db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response, request, url_for
from models.base_models import Provider, Appointment, Service, Client, User, Session
from flask import abort

app = Flask(__name__)
app.config['SECRETE_KEY'] = '16b0c77ece0958b3a5914bc951c1961e106ecbb511141f10515dee07b5e4453113c9'


@app.route('/', methods=['GET'], strict_slashes=False)
def this_status():
    return jsonify({"status": "Ok"})

@app.route('/appoms', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/appoms/provider-signup', methods=['GET', 'POST'], strict_slashes=False)
def provider_signup():
    if request.method == 'POST':
        username = request.form['username']
        business_name = request.form['business-name']
        business_address = request.form['business-address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        if confirm_password != password:
            return render_template('provider_signup.html', error="Password does not match.")
        with Session() as session:
            existing_users = session.query(User).filter_by(username=username).first()
            if existing_users:
                return render_template('provider_signup.html', error="Username already exist.")
            new_provider = Provider(username=username, business_name=business_name,
                                business_address=business_address, email=email, password=password, phone_number=phone_number)
            new_user = User(username=username, email=email, password=password, phone_number=phone_number)
            session.add(new_provider)
            session.add(new_user)
            session.commit()
            return render_template('success.html', username=username)
    return render_template('provider_signup.html') 

@app.route('/appoms/client-signup', methods=['GET', 'POST'], strict_slashes=False)
def client_signup():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        if confirm_password != password:
            return render_template('provider_signup.html', error="Password does not match.")
        with Session() as session:
            existing_users = session.query(User).filter_by(username=username).first()
            if existing_users:
                return render_template('provider_signup.html', error="Username already exist.")
            new_client = Client(username=username, first_name=first_name, last_name=last_name, email=email,
                                password=password, phone_number=phone_number)
            new_user = User(username=username, email=email, password=password, phone_number=phone_number)
            session.add(new_client)
            session.add(new_user)
            session.commit()
            return render_template('success.html', username=username)
    return render_template('provider_signup.html') 
@app.route('/appoms/contacts', methods=['GET'], strict_slashes=False)
def contacts():
    return render_template('contacts.html') 

@app.route('/appoms/about', methods=['GET'], strict_slashes=False)
def about():
    return render_template('about.html')

@app.route('/appoms/services', methods=['GET'], strict_slashes=False)
def services():
    return render_template('services.html')

@app.route('/appoms/signUp', methods=['GET', 'POST'], strict_slashes=False)
def signUp():
    return render_template('sign_up.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
