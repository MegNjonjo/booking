from flask import Flask, render_template, url_for
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
    return render_template('register.html', title='Register', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/services")
def services():
    return render_template('services.html', title='Services')



@app.route("/wellness packages")
def wellness():
    return "<h1>This is my wellness page</h1>"

if __name__ == '__main__':
    app.run(debug=True)