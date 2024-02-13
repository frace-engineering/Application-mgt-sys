from models.base_models import Session, User, Provider, Client, Service, Appointment

class CreateNew:
    def create_user():
        def __init__(self, username, email, password, phone_number):
            self.username = request.form['username']
            self.email = request.form['email']
            self.password = request.form['password']
            self.confirm_password = request.form['confirm_password']
            self.phone_number = request.form['phone_number']

            if self.confirm_password != self.password:
                return render_template('sign_up.html', error="Password does not match.")
            with Session() as session:
                existing_users = session.query(User).filter_by(username).first()
                if existing_users:
                    return render_template('sign_up', error="Username already exist.")
                new_user = User(username=username, email=email, password=password, phone_number=phone_number)
                session.add(new_user)
                session.commit()


