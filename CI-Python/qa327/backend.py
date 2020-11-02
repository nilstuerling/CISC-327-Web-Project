from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError

"""
This file defines all backend logic that interacts with database and other services
"""

# Function that validates user input email.
# Uses 3rd party libary email_validator for email validation.
def validateEmail(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError as e:
        return False

# Function that validates user input password
def validatePassword(password):
    # Check password length
    if len(password) < 6:
        return False
    # Check password contains at least 1 uppercase character
    if not any(char.isupper() for char in password):
        return False
    # Check password contains at least 1 lowercase character
    if not any(char.islower() for char in password):
        return False
    # Check password contains at least 1 character that is not alphanumeric (i.e. special character, including whitespace)
    if not any(char.isalnum() for char in password):
        return False
    return True



def get_user(email):
    """
    Get a user by a given email
    :param email: the email of the user
    :return: a user that has the matched email address
    """
    user = User.query.filter_by(email=email).first()
    return user


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
    new_user = User(email=email, name=name, password=hashed_pw)

    db.session.add(new_user)
    db.session.commit()
    return None


def get_all_tickets():
    return []