from qa327.models import db, User
from qa327.models import db, Tickets
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all backend logic that interacts with database and other services
"""



# Function that returns User object from database from unique email adress
def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user

# Logs user in session if valid email/password pair
def login_user(email, password):
    """
    Check user authentication by comparing the password
    :param email: the email of the user
    :param password: the password input
    :return: the user if login succeeds
    """
    # if this returns a user, then the name already exists in database
    user = get_user(email)
    if not user or not check_password_hash(user.password, password):
        return None
    return user

# Registers and adds user to database with valid supplied parameters
def register_user(email, name, password, password2):
    """
    Register the user to the database
    :param email: the email of the user
    :param name: the name of the user
    :param password: the password of user
    :param password2: another password input to make sure the input is correct
    :return: an error message if there is any, or None if register succeeds
    """

    hashed_pw = generate_password_hash(password, method='sha256')
    # store the encrypted password rather than the plain password
    new_user = User(email=email, name=name, password=hashed_pw, balance=5000)
    db.session.add(new_user)
    db.session.commit()
    return None

# Gets all tickets in tickets database and returns a list of all tickets
def get_all_tickets():
#    return []
     return db.session.query(Tickets).all()


# Adds ticket with input parameters and commits new addition to tickets database
def sell_ticket(name,quantity,price,expireDate):
    new_ticket = Tickets(email=User.email,name=name,date=expireDate,quantity=quantity,price=price)
    db.session.add(new_ticket)
    db.session.commit()
    return True

# Updates ticket with parameters and commits new changes to tickets database
def update_ticket(name,quantity,price,expireDate):
    updated_ticket = Tickets(email=User.email,name=name,date=expireDate,quantity=quantity,price=price)
    db.session.update(updated_ticket)
    db.session.commit()
    return True

# Adds specified ticket to user account, removing specified quantity from database
def buy_ticket(name,quantity):
    bought_ticket = Tickets(email=User.email,name=name,quantity=quantity)
    db.session.remove(bought_ticket)
    db.session.commit()
    return True
