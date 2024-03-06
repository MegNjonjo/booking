from datetime import datetime
from kijabe import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.user_loader
def load_user(doctor_id):
    return Doctor.query.get(int(doctor_id))

@login_manager.user_loader
def load_user(admin_id):
    return Admin.query.get(int(admin_id))

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='IMG_3.png')

    def __repr__(self):
        return f"Admin('{self.username}', '{self.email}', '{self.profile_pic}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='IMG_3.png')
    password = db.Column(db.String(60), nullable=False)
    feedbacks = db.relationship('Feedback', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}')"

class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='IMG_3.png')
    department = db.Column(db.String(60), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Doctor('{self.username}', '{self.email}', '{self.profile_pic}')"


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Appointment('{self.title}', '{self.date}', '{self.status}')"


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Feedback('{self.description}', '{self.date}')"

