from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']= 'ceddd47b15505bba706d169d651da11'

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

if __name__ == '__main__':
    app.run(debug=True)