from flask import render_template, url_for, flash, redirect, request
from kijabe import app, db, bcrypt
from kijabe.forms import RegistrationForm, LoginForm, DoctorForm, AdminForm, AppointmentForm, DoctorRegistrationForm
from kijabe.models import User, Feedback, Doctor, Admin, Appointment
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('user/register.html', title='Register', form=form)


@app.route("/registration/", methods=['GET', 'POST'])
def admin_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        admin = Admin(email=form.email.data, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/register.html', title='Register', form=form)


@app.route("/user/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('user_dashboard'))

    if form.validate_on_submit():
        print("Form data:", form.email.data, form.password.data)
        user = User.query.filter_by(email=form.email.data).first()
        print("User object:", user)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("password check passed")
            login_user(user, remember=form.remember.data)
            print("After login user")
            return redirect(url_for('user_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print("Flash message set")
    return render_template('user/login.html', title='Login', form=form)


@app.route("/user/dashboard")
def user_dashboard():
    return render_template('user/dashboard.html', title='User Dashboard')


@app.route("/admin/", methods=['GET', 'POST'])
def admin_login():
    form = AdminForm()
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))

    if form.validate_on_submit():
        print("Form data:", form.email.data, form.password.data)
        admin = Admin.query.filter_by(email=form.email.data).first()
        print("User object:", admin)
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            print("password check passed")
            login_user(admin, remember=form.remember.data)
            print("After login user")
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            print("Flash message set")
    return render_template('admin/login.html', title='Login', form=form)

@app.route("/admin/dashboard/")
def admin_dashboard():
    return render_template('admin/dashboard.html', title='Admin Dashboard')

@app.route("/dashboard/get_all_user", methods=['GET', 'POST'])
@login_required
def admin_get_all_user():
    users=User.query.all()
    return render_template('admin/users.html', title='Approve User', users=users)


@app.route("/dashboard/register_doctor", methods=['GET', 'POST'])
@login_required
def register_doctor():
    form = DoctorRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doctor = Doctor(username=form.username.data, email=form.email.data, department=form.department.data,
                        contact=form.contact.data, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        flash('The doctor account has been created!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        print("Form validation errors:", form.errors)
    return render_template('admin/register.html', title='Register Doctor', form=form)


@app.route("/dashboard/get_all_doctor", methods=['GET', 'POST'])
@login_required
def admin_get_all_doctor():
    doctors=Doctor.query.all()
    return render_template('admin/all_doctors.html', title='Approve User', doctors=doctors)


@app.route("/doctor/", methods=['GET', 'POST'])
def doctor_login():
    form = DoctorForm()
    if current_user.is_authenticated:
        return redirect(url_for('doctor_dashboard'))

    if form.validate_on_submit():
        print("Form data:", form.email.data, form.password.data)
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        print("User object:", doctor)
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            print("After login user")
            return redirect(url_for('doctor_dashboard'))
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'danger')
            print("Flash message set")
    return render_template('doctor/login.html', title='Doctor', form=form)


@app.route("/doctor/dashboard", methods=['GET', 'POST'])
def doctor_dashboard():
    return render_template('doctor/dashboard.html', title='Doctor Dashboard')



@app.route("/dashboard/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



appointments = []
def is_available(doctor_id, date):

    appointment = Appointment.query.filter_by(doctor_id=doctor_id, date=date).all()
    if appointment:
        flash('This slot is not available. Please choose a different date.', 'danger')
        return False
    else:
        return True


@app.route("/dashboard/book_appointment", methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    if form.validate_on_submit():
        if is_available(form.doctor_id.data, form.date.data):
            appointment = Appointment(title=form.title.data, description=form.description.data, date=form.date.data, doctor_id=form.doctor_id.data)
            db.session.add(appointment)
            db.session.commit()
            flash('Appointment booked successfully!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            return f'This slot is not available'
    return render_template('user/appointments.html', title='Book Appointment', form=form)


def is_available(date, time):
    for appointment in appointments:
        if appointment['date'] == date and appointment['time'] == time:
            return False
        return True


    if is_available(date, time):
        new_appointment = Appointment(title=title, date=date, status='Booked')
        db.session.add(new_appointment)
        db.session.commit()
        return redirect(url_for('user_dashboard'))
    else:
        return f'This slot is not available'


@app.route("/doctor/view_appointments")
def view_appointments():

    return render_template('doctor/appointments.html', title='View Appointments', appointments=appointments)

def is_available(date, time):
        for appointment in appointments:
            if appointment['date'] == date and appointment['time'] == time:
                return False
            return True


@app.route("/dashboard/my_appointments", methods=['GET', 'POST'])
@login_required
def my_appointments():
    appointments=Appointment.query.all()
    return render_template('user/all_appointments.html', title='Get Appointments', appointments=appointments)
