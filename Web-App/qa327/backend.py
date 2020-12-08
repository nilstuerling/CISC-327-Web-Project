from qa327.models import db, User
from qa327.models import db, Tickets
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from datetime import datetime

"""
This file defines all backend logic that interacts with database and other services
"""


# Function that validates ticket names
def validateTicketName(ticketName):
    # Check ticket name length (must be less than 60 characters)
    if len(ticketName) > 60:
        return False
    # Check if ticket name has leading or trailing space
    if ticketName[0] == ' ' or ticketName[-1] == ' ':
        return False
    # Check if ticket name is alphanumeric
    if not all((char.isalnum() or char == ' ') for char in ticketName):
        return False
    return True


# Function that validates that a ticket exists in the database
def validateTicketExists(ticketName):
    if not (Tickets.query.filter_by(name=ticketName).first()):
        return False
    return True


# Function that validates ticket quantity
def validateTicketQuantity(ticketQuantity):
    # Check quantity of ticket is more than 0 and max at 100
    if ticketQuantity <= 0 or ticketQuantity > 100:
        return False
    return True


# Function that validates if there are enough tickets to buy
def validateEnoughTickets(buyQuantity, ticketName):
    tmp = Tickets.query.filter_by(name=ticketName).first()
    return buyQuantity <= tmp.quantity


# Function that validates if the user has enough money to buy tickets
def validateBalanceEnough(buyQuantity, ticketName, user):
    tmp = Tickets.query.filter_by(name=ticketName).first()
    return user.balance >= ((buyQuantity * tmp.price) * 1.35) * 1.05 # service fee: 1.35 (35%), tax: 1.05 (5%)


# Function that validates ticket price
def validateTicketPrice(ticketPrice):
    # Check ticket price is within 10 - 100
    if not (10 <= ticketPrice <= 100):
        return False
    return True


# Function that validates ticket expiry date
def validateTicketExpiryDate(date):
    if len(date) != 8:
        return False
    year = date[0:4]
    month = date[4:6]
    day = date[6:]
    dateString = year + "-" + month + "-" + day
    today = datetime.today().date()
    try:
        ticketDate = datetime.strptime(dateString, "%Y-%m-%d").date()
        if (ticketDate < today):
            return False
        return True
    except ValueError as e:
        print(e)
        return False


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
     return db.session.query(Tickets).all()


# Adds ticket with input parameters and commits new addition to tickets database
def sell_ticket(userEmail, name, quantity, price, expireDate):
    try:
        formattedDate = format_date(expireDate)
        new_ticket = Tickets(email=userEmail, name=name,date=formattedDate,quantity=quantity,price=price)
        db.session.add(new_ticket)
        db.session.commit()
    except Exception as e:
        return str(e)
    return ""


# Updates ticket with parameters and commits new changes to tickets database
def update_ticket(userEmail,name,quantity,price,expireDate):
    formattedDate = format_date(expireDate)
    updated_ticket = Tickets(email=userEmail,name=name,date=formattedDate,quantity=quantity,price=price)
    db.session.update(updated_ticket)
    db.session.commit()
    return True


# Adds specified ticket to user account, removing specified quantity from database
def buy_ticket(userEmail,name,quantity):
    bought_ticket = Tickets(email=userEmail,name=name,quantity=quantity)
    db.session.remove(bought_ticket)
    db.session.commit()
    return True


# Formats date from string input into printable string
def format_date(ticketDate):
    year = ticketDate[0:4]
    month = ticketDate[4:6]
    day = ticketDate[6:]
    return day + "/" + month + "/" + year
