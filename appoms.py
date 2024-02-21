#!/usr/bin/python3
from datetime import datetime
import uuid
from models.db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response, request, url_for, redirect, flash
from flask import session
from markupsafe import escape
from models.base_models import Provider, Appointment, Service, Client, User, Admin, Session
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '16b0c77ece0958b3a5914bc951c1961e106ecbb511141f10515dee07b5e4453113c9'


@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/signUp', methods=['GET', 'POST'], strict_slashes=False)
def signUp():
    return render_template('sign_up.html')

@app.route('/dashboard/admin', methods=['GET', 'POST'], strict_slashes=False)
def creat_admin():
    if request.method == 'POST':
        session['username'] = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']
        username = session['username']
        with Session() as db_session:
            existing_users = db_session.query(Admin).filter_by(username=username).first()
            if existing_users:
                flash("Pasword does not match", "info")
                return render_template('admin.html')
            new_user = User(username=username, email=email, password=password,
                        created_at=datetime.utcnow(), phone_number=phone_number)
            new_admin = Admin(username=username, email=email, password=password,
                        created_at=datetime.utcnow(), phone_number=phone_number)
            db_session.add(new_admin)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('dashboard', user_id=new_user.id))
    return render_template('/dashboard/admin.html')

@app.route('/appoms/provider_signup', methods=['GET', 'POST'], strict_slashes=False)
def provider_signup():
    if request.method == 'POST':
        session['username'] = request.form['username']
        provider_name = request.form['business-name']
        provider_address = request.form['business-address']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        username = session['username']
        if confirm_password != password:
            flash("Pasword does not match", "info")
            return render_template('provider_signup.html')
        with Session() as db_session:
            existing_users = db_session.query(User).filter_by(username=username).first()
            if existing_users:
                flash("Pasword does not match", "info")
                return render_template('provider_signup.html')
            new_user = User(username=username, email=email, password=password,
                        created_at=datetime.utcnow(), phone_number=phone_number)
            new_provider = Provider(username=username, provider_name=provider_name,
                            provider_address=provider_address, email=email, password=password,
                            phone_number=phone_number, users=new_user)
            db_session.add(new_provider)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('user', user_id=new_user.id))
    return render_template('provider_signup.html') 

@app.route('/appoms/client_signup', methods=['GET', 'POST'], strict_slashes=False)
def client_signup():
    if request.method == 'POST':
        session['username'] = request.form['username']
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']

        username = session['username']
        if confirm_password != password:
            flash("Error! Password does not match.", "info")
            return remder_template('client_signup.html')
        with Session() as db_session:
            existing_users = db_session.query(User).filter_by(username=username).first()
            if existing_users:
                flash("Error! Username already exist.", "info")
                return render_template('client_signup.html')
            new_user = User(username=username, email=email, password=password, phone_number=phone_number)
            new_client = Client(username=username, first_name=first_name, last_name=last_name, email=email, password=password, phone_number=phone_number, users=new_user)
            db_session.add(new_client)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for('user', user_id=new_user.id))
    return render_template('client_signup.html') 

@app.route('/user_login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        username = session['username']
        password = request.form['password']
        with Session() as db_session:
            current_user = db_session.query(User).filter_by(username=username).first()
            if not current_user:
                flash("Error! User does not exist", "info")
                return redirect(url_for('login'))
            if  password == current_user.password:
                if current_user.username == 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('user', user=user))
            else:
                flash("Error! User does not exist", "info")
                return redirect(url_for('login'))
    return render_template('login.html') 

@app.route('/dashboard/user', methods=['GET'], strict_slashes=False)
def user():
    if 'username' in session:
        username = session['username']
        with Session() as db_session:
            providerUser = db_session.query(Provider).filter_by(username=username).first()
            if providerUser:
            #this_user = session.query(User).filter_by(user=user).first()
                userName = providerUser.username
                userId = providerUser.id
                providerName = providerUser.provider_name
                providerAddr = providerUser.provider_address
                phoneNumber = providerUser.phone_number
                email = providerUser.email
                clients = db_session.query(Client).filter_by(provider_id=userId).all()
                return render_template('/dashboard/providers/index.html', clients=clients, userName=userName, userId=userId,
                    providerName=providerName, providerAddr=providerAddr, email=email, phoneNumber=phoneNumber)
            clientUser = db_session.query(Client).filter_by(username=username).first()
            if clientUser:
            #this_user = session.query(User).filter_by(user=user).first()
                userName = clientUser.username
                userId = clientUser.id
                firstName = clientUser.first_name
                lastName = clientUser.last_name
                phoneNumber = clientUser.phone_number
                email = clientUser.email
                providers = db_session.query(Provider).all()
                return render_template('/dashboard/clients/index.html', providers=providers,
                        userName=userName, userId=userId,
                    firstName=firstName, lastName=lastName, phoneNumber=phoneNumber)
            return f"Not found {user}"

@app.route('/dashboard/services/create', methods=['GET', 'POST'], strict_slashes=False)
def create_service():
    if request.method == 'POST':
        service_name = request.form['service-name']
        description = request.form['description']
        with Session() as db_session:
            new_service = Service(service_name=service_name, description=description)
            db_session.add(new_service)
            db_session.commit()
            return redirect(url_for('services'))
    return render_template('/dashboard/services/new.html')

@app.route('/dashboard/services', methods=['GET'], strict_slashes=False)
def services():
    with Session() as db_session:
        services = db_session.query(Service).all()
    return render_template('/dashboard/services/index.html', services=services)

@app.route('/dashboard', methods=['GET'], strict_slashes=False)
def dashboard():
    with Session() as db_session:
        usersCount = db_session.query(User).count()
        providersCount = db_session.query(Provider).count()
        clientsCount = db_session.query(Client).count()
        servicesCount = db_session.query(Service).count()
        appointmentsCount = db_session.query(Appointment).count()
    return render_template('/dashboard/index.html', usersCount=usersCount, providersCount=providersCount,
            clientsCount=clientsCount, servicesCount=servicesCount, appointmentsCount=appointmentsCount)

@app.route('/dashboard/users', methods=['GET'], strict_slashes=False)
def users():
    with Session() as db_session:
        users = db_session.query(User).all()
    return render_template('/dashboard/users/index.html', users=users)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
