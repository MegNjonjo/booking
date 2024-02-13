from flask import render_template, url_for, flash, redirect
from kijabe import app
from kijabe.forms import RegistrationForm, LoginForm
from kijabe.models import User, Feedback

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@collections.com' and form.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/services")
def services():
    return render_template('services.html', title='Services')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')


@app.route("/wellness packages")
def wellness():
    return "<h1>This is my wellness page</h1>"