from flask import render_template, url_for, flash, redirect, request
from kijabe import app, db, bcrypt
from kijabe.forms import RegistrationForm, LoginForm, DoctorForm
from kijabe.models import User, Feedback, Doctor
from flask_login import login_user, current_user, logout_user

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)

@app.route("/doctor_view", methods=['GET', 'POST'])
def doctor():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('doctor.html', appointments=appointments, title='Doctor', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/services")
def services():
    return render_template('services.html', title='Services')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route("/wellness packages")
def wellness():
    return "<h1>This is my wellness page</h1>"


appointments = []

'''@app.route("/book_appointment")
def book_appointment():
    if request.method == 'POST':
        date = request.form['date']
        time = request.form['time']

        if is_available(date, time):
            appointment = {'date': date, 'time': time}
            appointments.append(appointment)
            return redirect(url_for('index'))
        else:
            return f'This slot is not available'

def is_available(date, time):
    for appointment in appointments:
        if appointment['date'] == date and appointment['time'] == time:
            return False
        return True

'''