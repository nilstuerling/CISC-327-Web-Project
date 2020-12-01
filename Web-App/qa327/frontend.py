from flask import render_template, request, session, redirect, url_for
from qa327 import app
from datetime import date
from datetime import datetime
import qa327.backend as bn

"""
This file defines the front-end part of the service.
It elaborates how the services should handle different
http requests from the client (browser) through templating.
The html templates are stored in the 'templates' folder. 
"""


# renders register page
@app.route('/register', methods=['GET'])
def register_get():
    # Check if there is an existing logged in user
    if "logged_in" in session:
        email = session['logged_in']
        user = bn.get_user(email)

        if user:
            return redirect('/')    # redirect to user profile page
        else:
            return redirect('/logout')  # log out of invalid session

    return render_template('register.html', message='')


# validates register info from form, and calls backend to add user to database
@app.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    error_message = None

    if password != password2:
        error_message = "Password format is incorrect"

    elif not bn.validateEmail(email):
        error_message = "Email format is incorrect"

    elif not bn.validatePassword(password):
        error_message = "Password format is incorrect"

    elif not bn.validateUserName(name):
        error_message = "Username format is incorrect"
    else:
        user = bn.get_user(email)
        if user:
            error_message = "This email has been ALREADY used"
        elif bn.register_user(email, name, password, password2):
            error_message = "Failed to store user info."
    # if there is any error messages when registering new user
    # at the backend, go back to the register page.
    if error_message:
        return render_template('register.html', message=error_message)
    else:
        return redirect('/login')


# renders login page
@app.route('/login', methods=['GET'])
def login_get():
    if "logged_in" in session:
        email = session['logged_in']
        user = bn.get_user(email)

        if user:
            return redirect('/')  # redirect to user profile page
        else:
            return redirect('/logout')  # log out of invalid session
    return render_template('login.html', message='Please login')


# logs user in session if valid email/password pair, present in databse
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    emailIsValid = bn.validateEmail(email)
    passwordIsValid = bn.validatePassword(password)

    if not emailIsValid or not passwordIsValid:
        return render_template('login.html', message='Email/Password format is incorrect')

    user = bn.login_user(email, password)
    if user:
        session['logged_in'] = user.email
        """
        Session is an object that contains sharing information 
        between browser and the end server. Typically it is encrypted 
        and stored in the browser cookies. They will be past 
        along between every request the browser made to this services.

        Here we store the user object into the session, so we can tell
        if the client has already login in the following sessions.

        """
        # success! go back to the home page
        # code 303 is to force a 'GET' request
        return redirect('/', code=303)
    else:
        return render_template('login.html', message='Email/Password combination incorrect')


# logs current user out of session
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


# Function decoration to validate logged in session
def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object

    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.

    To wrap a function, we can put a decoration on that function.
    Example:

    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            user = bn.get_user(email)
            if user:
                # if the user exists, call the inner_function
                # with user as parameter
                return inner_function(user)
            else:
                return redirect('/logout')
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    wrapped_inner.__name__ = inner_function.__name__
    return wrapped_inner

# Renders logged in user home page
@app.route('/')
@authenticate
def profile(user):
    # authentication is done in the wrapper function
    # see above.
    # by using @authenticate, we don't need to re-write
    # the login checking code all the time for other
    # front-end portals
    sellErrorMessage = ""
    if "sellErrorMessage" in request.args:
        sellErrorMessage = request.args["sellErrorMessage"]
    buyErrorMessage = ""
    if "buyErrorMessage" in request.args:
        buyErrorMessage = request.args["buyErrorMessage"]
    updateErrorMessage = ""
    if "updateErrorMessage" in request.args:
        updateErrorMessage = request.args["updateErrorMessage"]

    tickets = bn.get_all_tickets()
    for ticket in tickets:
        date1 = date.today()
        date2 = datetime.strptime(ticket.date, "%d/%m/%Y").date()
        if (date1 > date2 and date1 != date2):
            tickets.remove(ticket)
    return render_template('index.html', user=user, tickets=tickets, sellErrorMessage=sellErrorMessage, buyErrorMessage=buyErrorMessage, updateErrorMessage=updateErrorMessage)

# gets ticket info from form
@app.route('/sell', methods=['POST'])
@authenticate
def sell_form_post(user):
    name = request.form.get('name')
    quantity = int(request.form.get('quantity'))
    price = int(request.form.get('price'))
    expireDate = request.form.get('expireDate')
    sellErrorMessage = None
    if not(bn.validateTicketName(name)):
        sellErrorMessage = "Invalid ticket name"
    elif not(bn.validateTicketQuantity(quantity)):
        sellErrorMessage = "Invalid ticket quantity"
    elif not(bn.validateTicketPrice(price)):
        sellErrorMessage = "Invalid ticket price"
    elif not(bn.validateTicketExpiryDate(expireDate)):
        sellErrorMessage = "Invalid ticket expiry date"

    if sellErrorMessage:
        return redirect(url_for('.profile', sellErrorMessage=sellErrorMessage))

    bn.sell_ticket(user.email, name, quantity, price, expireDate)
    return redirect('/')


@app.route('/sell', methods=['GET'])
def sell_form_get():
	if 'logged_in' in session:
		return redirect('/')
	else:
		return redirect('/login')

# Gets ticket info from form
@app.route('/buy', methods=['POST'])
@authenticate
def buy_form_post(user):
    name = request.form.get('buyName')
    quantity = int(request.form.get('buyQuantity'))
    buyErrorMessage = None
    if not(bn.validateTicketName(name)):
        buyErrorMessage = "Invalid ticket name"
    elif not(bn.validateTicketQuantity(quantity)):
        buyErrorMessage = "Invalid ticket quantity"
    
    # Add validation for:
    # - The ticket name exists in the database and the quantity is more than the quantity requested to buy
    # - The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)

    if buyErrorMessage:
        return redirect(url_for('.profile', buyErrorMessage=buyErrorMessage))

    bn.buy_ticket(user.email, name, quantity)
    return redirect('/')


@app.route('/buy', methods=['GET'])
def buy_form_get():
	if 'logged_in' in session:
		return redirect('/')
	else:
		return redirect('/login')

# gets ticket info from form and renders update ticket page
@app.route('/update', methods=['POST'])
@authenticate
def update_form_post(user):
    name = request.form.get('updateName')
    quantity = int(request.form.get('updateQuantity'))
    price = int(request.form.get('updatePrice'))
    expireDate = request.form.get('updateExpireDate')
    updateErrorMessage = None
    if not(bn.validateTicketName(name)):
        updateErrorMessage = "Invalid ticket name"
    elif not(bn.validateTicketQuantity(quantity)):
        updateErrorMessage = "Invalid ticket quantity"
    elif not(bn.validateTicketPrice(price)):
        updateErrorMessage = "Invalid ticket price"
    elif not(bn.validateTicketExpiryDate(expireDate)):
        updateErrorMessage = "Invalid ticket expiry date"
    elif not (bn.validateExistsTicketName(name)):
        updateErrorMessage = "Invalid ticket name does not exist"
    if updateErrorMessage:
        return redirect(url_for('.profile', updateErrorMessage=updateErrorMessage))

    bn.update_ticket(user.email, name, quantity, price, expireDate)
    return redirect('/')

@app.route('/update', methods=['GET'])
def update_form_get():
	if 'logged_in' in session:
		return redirect('/')
	else:
		return redirect('/login')

# 404 error
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
