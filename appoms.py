#!/usr/bin/python3
from datetime import datetime
import uuid
from models.db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response, request, url_for, redirect, flash
from models.base_models import Provider, Appointment, Service, Client, User, Session
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '16b0c77ece0958b3a5914bc951c1961e106ecbb511141f10515dee07b5e4453113c9'


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/signUp', methods=['GET', 'POST'], strict_slashes=False)
def signUp():
    return render_template('sign_up.html')

@app.route('/appoms/provider_signup', methods=['GET', 'POST'], strict_slashes=False)
def provider_signup():
    if request.method == 'POST':
        username = request.form['username']
        provider_name = request.form['business-name']
        provider_address = request.form['business-address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        if confirm_password != password:
            flash("Pasword does not match", "error")
            return render_template('provider_signup.html')
        with Session() as session:
            existing_users = session.query(User).filter_by(username=username).first()
            if existing_users:
                flash("Pasword does not match", "error")
                return render_template('provider_signup.html')
            new_user = User(username=username, email=email, password=password, created_at=datetime.utcnow(), phone_number=phone_number)
            new_provider = Provider(username=username, provider_name=provider_name, provider_address=provider_address, email=email, password=password, phone_number=phone_number, users=new_user)
            session.add(new_provider)
            session.add(new_user)
            session.commit()
            return redirect(url_for('dashboard'))
    return render_template('provider_signup.html') 

@app.route('/appoms/client_signup', methods=['GET', 'POST'], strict_slashes=False)
def client_signup():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        if confirm_password != password:
            flash("Error! Password does not match.", "error")
            return remder_template('client_signup.html')
        with Session() as session:
            existing_users = session.query(User).filter_by(username=username).first()
            if existing_users:
                flash("Error! Username already exist.", "error")
                return render_template('client_signup.html')
            new_user = User(username=username, email=email, password=password, phone_number=phone_number)
            new_client = Client(username=username, first_name=first_name, last_name=last_name, email=email, password=password, phone_number=phone_number, users=new_user)
            session.add(new_client)
            session.add(new_user)
            session.commit()
            return redirect(url_for('dashboard'))
    return render_template('client_signup.html') 

@app.route('/user_login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        with Session() as session:
            current_user = session.query(User).filter_by(email=email).first()
            if not current_user:
                flash("Error! User does not exist", "error")
                return redirect(url_for('login'))
            if  password == current_user.password:
                return redirect(url_for('dashboard'))
            else:
                flash("Error! User does not exist", "error")
                return redirect(url_for('login'))
    return render_template('login.html') 

@app.route('/dashboard/services/create', methods=['GET', 'POST'], strict_slashes=False)
def create_service():
    if request.method == 'POST':
        service_name = request.form['service-name']
        description = request.form['description']
        with Session() as session:
            new_service = Service(service_name=service_name, description=description)
            session.add(new_service)
            session.commit()
            return redirect(url_for('services'))
    return render_template('/dashboard/services/new.html')

@app.route('/dashboard/services', methods=['GET'], strict_slashes=False)
def services():
    with Session() as session:
        services = session.query(Service).all()
    return render_template('/dashboard/services/index.html', services=services)

@app.route('/dashboard', methods=['GET'], strict_slashes=False)
def dashboard():
    with Session() as session:
        usersCount = session.query(User).count()
        providersCount = session.query(Provider).count()
        clientsCount = session.query(Client).count()
        servicesCount = session.query(Service).count()
        appointmentsCount = session.query(Appointment).count()
    return render_template('/dashboard/index.html', usersCount=usersCount, providersCount=providersCount,
            clientsCount=clientsCount, servicesCount=servicesCount, appointmentsCount=appointmentsCount)

@app.route('/dashboard/users', methods=['GET'], strict_slashes=False)
def users():
    with Session() as session:
        users = session.query(User).all()
    return render_template('/dashboard/users/index.html', users=users)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
