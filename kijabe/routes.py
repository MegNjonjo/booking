from flask import render_template, url_for, flash, redirect, request
from kijabe import app, db, bcrypt
from kijabe.forms import RegistrationForm, LoginForm, DoctorForm, AdminForm, AppointmentForm
from kijabe.models import User, Feedback, Doctor, Admin, Appointment
from flask_login import login_user, current_user, logout_user

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('user/register.html', title='Register', form=form)


@app.route("/user/", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user/dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('user/login.html', title='Login', form=form)


@app.route("/login/dashboard")
def user_dashboard():

    return render_template('user/dashboard.html', title='User Dashboard')


@app.route("/admin/", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated:
        return redirect(url_for('admin/dashboard'))
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if form.email.data == 'megnjonjo@gmail.com' and form.password.data == 'testing':
            flash(f'You have been logged in!', 'success')
            if admin and bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin, remember=form.remember.data)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', appointments=appointments, title='Admin', form=form)

@app.route("/login/dashboard", methods=['POST'])
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin')


@app.route("/doctor/", methods=['GET', 'POST'])
def doctor():
    if current_user.is_authenticated:
        return redirect(url_for('doctor/dashboard'))
    form = DoctorForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            return redirect(url_for('doctor_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('doctor/login.html', appointments=appointments, title='Doctor', form=form)


@app.route("/login/dashboard", methods=['POST'])
def doctor_dashboard():
    return render_template('doctor/dashboard.html', title='Doctor')




@app.route("/dashboard/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/services")
def services():
    return render_template('services.html', title='Services')




@app.route("/wellness packages")
def wellness():
    return "<h1>This is my wellness page</h1>"


appointments = []

@app.route("/dashboard/book_appointment", methods=['GET', 'POST'])
def book_appointment():
    form = AppointmentForm()
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


@app.route("/doctor/view_appointments")
def view_appointments():

    return render_template('doctor/appointments.html', title=title, appointments=appointments)

def is_available(date, time):
        for appointment in appointments:
            if appointment['date'] == date and appointment['time'] == time:
                return False
            return True



