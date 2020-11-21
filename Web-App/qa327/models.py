from qa327 import app
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError

"""
This file defines all models used by the server
These models provide us a object-oriented access
to the underlying database, so we don't need to 
write SQL queries such as 'select', 'update' etc.
"""


db = SQLAlchemy()
db.init_app(app)


# User object, stores user information in database
class User(db.Model):
    """
    A user model which defines the sql table
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    balance = db.Column(db.Numeric(scale=2))



# Ticket object, stores ticket info in databse
class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(1000))
    date = db.Column(db.String(1000))
    quantity = db.Column(db.String(100))
    price = db.Column(db.String(10000))


# it creates all the SQL tables if they do not exist
with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
