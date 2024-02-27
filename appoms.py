#!/usr/bin/python3
"""Import all the packages required"""
from datetime import datetime
from os import getenv
import uuid
from sqlalchemy import or_
from werkzeug.security import generate_password_hash, check_password_hash
from models.db_storage import DBStorage as DB
from flask import Flask, jsonify, render_template, make_response, request, url_for, redirect, flash
from flask import session
from markupsafe import escape
from models.base_models import Provider, Appointment, Service, Client, User, Admin, Session, Slot
from flask import abort
from flask_login import current_user, UserMixin, LoginManager, login_user, login_required, logout_user

app = Flask(__name__)
"""Config the secret key for browser session """
app.config['SECRET_KEY'] = '16b0c77ece0958b3a5914bc951c1961e106ecbb511141f10515dee07b5e4453113c9'
#app.config['SECRET_KEY'] = APPOMS_KEY
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


"""The landing page route of appoms"""
@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    return render_template('index.html') 

@app.route('/contact_us', methods=['GET'], strict_slashes=False)
def contact():
    return render_template('contact_us.html') 

@app.route('/signUp', methods=['GET', 'POST'], strict_slashes=False)
def signUp():
    """Render the sign uo page"""
    return render_template('sign_up.html')

@app.route('/dashboard/admin', methods=['GET', 'POST'], strict_slashes=False)
def creat_admin():
    """This code block will be used to bt existing admin to add another admin"""
    if request.method == 'POST':
        session['username'] = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm-password']
        phone_number = request.form['phone-number']
        username = session['username']
        if password != confirm_password:
            return render_template('admin.html', error="Mismatched password")
        with Session() as db_session:
            existing_users = db_session.query(Admin).filter_by(username=username).first()
            if existing_users:
                return render_template('/dashboard/admin.html', error="User already exist")
            new_user = User(username=username, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'),
                    created_at=datetime.utcnow(), phone_number=phone_number)
            new_admin = Admin(username=username, email=email, created_at=datetime.utcnow(), phone_number=phone_number,
                    user_id=new_user.id, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db_session.add(new_admin)
            db_session.add(new_user)
            db_session.commit()
            return render_template('welcome.html', username=new_user.username)
    return render_template('/dashboard/admin.html')

@app.route('/provider_signup', methods=['GET', 'POST'], strict_slashes=False)
def provider_signup():
    """Method to sign up and authenticate a service provider"""
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
                return render_template('provider_signup.html')
            new_user = User(username=username, email=email, created_at=datetime.utcnow(), phone_number=phone_number,
                    password=generate_password_hash(password, method="pbkdf2:sha256"))
            new_provider = Provider(username=username, provider_name=provider_name, provider_address=provider_address,
                    email=email, phone_number=phone_number, users=new_user, password=generate_password_hash(password, method="pbkdf2:sha256"))
            db_session.add(new_provider)
            db_session.add(new_user)
            db_session.commit()
            return render_template('welcome.html', username=new_user.username)
    return render_template('provider_signup.html') 

@app.route('/client_signup', methods=['GET', 'POST'], strict_slashes=False)
def client_signup():
    """Method to sign uo and authenticate a client"""
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
                return render_template('client_signup.html', error="User alrady exist")
            new_user = User(username=username, email=email, phone_number=phone_number, password=generate_password_hash(password, method='pbkdf2:sha256'))
            new_client = Client(username=username, first_name=first_name, last_name=last_name, email=email,
                    phone_number=phone_number, users=new_user, password=generate_password_hash(password, method='pbkdf2:sha256'))
            db_session.add(new_client)
            db_session.add(new_user)
            db_session.commit()
            return render_template('welcome.html', username=new_user.username)
    return render_template('client_signup.html') 

@app.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    """Existing user login method"""
    if request.method == 'POST':
        session['username'] = request.form['username']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        with Session() as db_session:
            username = session['username']
            this_user = db_session.query(User).filter_by(username=username).first()
            if not this_user:
                flash("Error! User does not exist")
                return redirect(url_for('login'))
            if  check_password_hash(this_user.password, password):
                if this_user.username == 'admin':
                    login_user(this_user, remember=remember)
                    return redirect(url_for('dashboard', current_user=this_user))
                else:
                    login_user(this_user, remember=remember)
                    return redirect(url_for('user', current_user=this_user))
            else:
                flash("Error! User does not exist")
                return redirect(url_for('login'))
    return render_template('login.html') 

@login_manager.user_loader
def load_user(user_id):
    with Session() as db_session:
        user_id = db_session.query(User).get(str(user_id))
        return user_id

@app.route('/dashboard/user', methods=['GET'], strict_slashes=False)
@login_required
def user():
    """Users dashboard"""
    #if current_user.is_active:
    username = request.args.get('username')
    if username is None:
        return redirect(url_for('login'))
    with Session() as db_session:
        providerUser = db_session.query(Provider).filter_by(username=username).first()
        if providerUser:
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
            userName = clientUser.username
            userId = clientUser.id
            firstName = clientUser.first_name
            lastName = clientUser.last_name
            phoneNumber = clientUser.phone_number
            email = clientUser.email
            providers = db_session.query(Provider).all()
            return render_template('/dashboard/clients/index.html', providers=providers, userName=userName,
                    userId=userId, email=email, firstName=firstName, lastName=lastName, phoneNumber=phoneNumber)
        return f"User not found {current_user.username}"

@app.route('/dashboard/services/create', methods=['GET', 'POST'], strict_slashes=False)
def create_service():
    if request.method == 'POST':
        service_name = request.form['service-name']
        description = request.form['description']
        with Session() as db_session:
            new_service = Service(service_name=service_name, description=description)
            db_session.add(new_service)
            db_session.commit()
            return redirect(url_for('services', providers=current_user))
    return render_template('/dashboard/services/new.html')

@app.route('/dashboard/services', methods=['GET'], strict_slashes=False)
def services():
    with Session() as db_session:
        services = db_session.query(Service).all()
    return render_template('/dashboard/services/index.html', services=services)

@app.route('/dashboard', methods=['GET'], strict_slashes=False)
@login_required
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

@app.route('/our_services', methods=['GET'], strict_slashes=False)
def our_services():
    return render_template('our_services.html')

@app.route('/slots', methods=['GET', 'POST'], strict_slashes=False)
@login_required
def createSlot():
    if request.method == 'POST':
        #provider_id = request.args.get('providers.id')
        week_day = request.form['week-day']
        start_time = request.form['start-time']
        end_time = request.form['end-time']
        with Session() as db_session:
            providers = db_session.query(Provider).filter_by(username=current_user.username).first()
            existing_slot = db_session.query(Slot).filter_by(week_day=week_day, start_time=start_time).first()
            if not existing_slot:
                new_slot = Slot(week_day=week_day, start_time=start_time, end_time=end_time, provider_id=providers.id)
                db_session.add(new_slot)
                db_session.commit()
                return render_template('/dashboard/appointments/index.html')
            if providers.id == existing_slot.provider_id:
                return f"Slot already booked."
            new_slot = Slot(week_day=week_day, start_time=start_time, end_time=end_time, provider_id=providers.id)
            db_session.add(new_slot)
            db_session.commit()
            return render_template('/dashboard/appointments/index.html')
    return render_template('/dashboard/appointments/slots.html', user_id=current_user.id)

@app.route('/view_slots', methods=['GET'], strict_slashes=False)
@login_required
def view_slot():
    user_id = request.args.get('user_id')
    with Session() as db_session:
        providers = db_session.query(Provider).filter_by(id=user_id).first()
        if providers:
            slots = db_session.query(Slot).filter_by(provider_id=providers.id).all()
            return render_template('/dashboard/appointments/clients.html', slots=slots)
        return f"No entry for this User {user_id}."

@app.route('/book_appointment', methods=['GET'], strict_slashes=False)
@login_required
def book_slot():
    slot_id = request.args.get('slot_id')
    user_id = request.args.get('user_id')
    with Session() as db_session:
        slot = db_session.query(Slot).filter_by(id=slot_id).first()
        #id = slot.provider_id
        #provider = db_session.query(Provider).filter_by(user_id=user_id).first()
        client = db_session.query(Client).filter_by(user_id=user_id).first()
        existing_appointment = db_session.query(Appointment).filter_by(slot_id=slot_id).first()
        if existing_appointment:
            return f"Slot already taken. Book for another slot"
        new_appointment = Appointment(week_day=slot.week_day, start_time=slot.start_time, end_time=slot.end_time,
                provider_id=slot.provider_id, client_id=client.id)
        db_session.add(new_appointment)
        db_session.commit()
        return render_template('/dashboard/appointments/client_booked_slot.html')

@app.route('/availableSlots', methods=['GET'], strict_slashes=False)
@login_required
def slot():
    provider_id = request.args.get('provider_id')
    #client_id = request.args.get('client_id')
    with Session() as db_session:
        providers = db_session.query(Provider).filter_by(username=current_user.username).first()
        #slots = db_session.query(Slot).filter(or_(Slot.provider_id == provider_id, Slot.client_id == client_id)).all()
        slots = db_session.query(Slot).filter_by(provider_id=providers.id).all()
        if slots:
            return render_template('/dashboard/appointments/index.html', slots=slots)
        return f"No entry found."


@app.route('/appointments', methods=['GET'], strict_slashes=False)
@login_required
def appointment():
    username = request.args.get('username')
    #slot_id = request.args.get('slot_id')
    with Session() as db_session:
        #provider = db_session.query(Provider).filter_by(user_id=user_id).all()
        client = db_session.query(Client).filter_by(username=username).all()
        appointments = db_session.query(Appointment).all()
        if appointments:
            if isinstance(current_user, Provider):
                return render_template('/dashboard/appointments/index.html', appointments=appointments)
            return render_template('/dashboard/appointments/clients.html', appointments=appointments)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, threaded=True, debug=True)
