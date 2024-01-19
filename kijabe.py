from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')


@app.route("/login")
def login():
    return "<h1>This is my Log In Page</h1>"

@app.route("/services")
def services():
    return render_template('services.html', title='Services')



@app.route("/wellness packages")
def wellness():
    return "<h1>This is my wellness page</h1>"

if __name__ == '__main__':
    app.run(debug=True)