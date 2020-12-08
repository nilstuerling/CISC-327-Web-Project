import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from qa327.backend import format_date
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the /sell endpoint.

The tests will only test the frontend portion of the /sell endpoint, and will patch the backend to return specific values for different test cases
"""

# Valid user login credentials
valid_test_user_email="test_frontend@test.com"
valid_test_user_password="Test_frontend!"

# Mock a sample user
test_user = User(
    id = 1,
    email=valid_test_user_email,
    name='test_frontend',
    password=generate_password_hash(valid_test_user_password),
    balance = 5000
)

# Mock sell ticket error (mocking business logic failure)
sell_ticket_error_message = "Unable to sell ticket"
sell_ticket_failure = Exception(sell_ticket_error_message)

# Invalid ticket name cases
ticket_name_not_alphanumeric = "B@dT1cket~"
ticket_name_with_leading_space = " ticketname"
ticket_name_with_trailing_space = "ticketname "
ticket_name_too_long = "ticketttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt"

# Invalid quantity cases
quantity_too_low = 0
quantity_too_high = 101

# Invalid price cases
price_too_low = 9
price_too_high = 101

# Invalid date cases
date_non_numeric = "2020 Dec 10"
date_from_the_past = "20191210"

# Valid input case
valid_ticket_name = "ticket name"
valid_quantity = 10
valid_price = 10
valid_date = "20221225"

@patch('qa327.backend.get_user', return_value=test_user)
class FrontEndSellTest(BaseCase):

    ### Helper functions ###

    # Opens /login and attempts login POST with information from supplied User object
    def login(self):
        self.open(base_url + '/login')
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)
        return self.click('input[type="submit"]')

    # Gets /logout and logs out current user if any
    def logout(self):
        self.get(base_url + '/logout')

    def submitSellForm(self, name, quantity, price, expireDate):
        self.type("#name", name)
        self.type("#quantity", quantity)
        self.type("#price", price)
        self.type("#expireDate", expireDate)
        return self.click('input[id="btn-submit"]')

    def startNewSession(self):
        self.logout()
        self.login()

        # Check that current page contains #welcome-header (i.e. redirected to user profile page)
        self.assert_element("#welcome-header")

    ########################
    

    # R4.1 Check if sell actions fail when ticket name is not alphanumeric or has leading/trailing spaces
    def test_ticket_name_alphanumeric_and_space_invalid(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(ticket_name_not_alphanumeric, valid_quantity, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket name", "#sellErrorMessage")

        # Submit sell form
        self.submitSellForm(ticket_name_with_leading_space, valid_quantity, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket name", "#sellErrorMessage")

        # Submit sell form
        self.submitSellForm(ticket_name_with_trailing_space, valid_quantity, valid_price, valid_date)
        
        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket name", "#sellErrorMessage")
    

    #R4.2 Check if sell actions fail when ticket name is longer than 60 characters
    def test_ticket_name_length_invalid(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(ticket_name_too_long, valid_quantity, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket name", "#sellErrorMessage")


    #R4.3 Check if sell actions fail when quantity of tickets is not within correct range >0, <=100
    def test_ticket_quantity_invalid(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(valid_ticket_name, quantity_too_low, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket quantity", "#sellErrorMessage")

        # Submit sell form
        self.submitSellForm(valid_ticket_name, quantity_too_high, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket quantity", "#sellErrorMessage")

    
    #R4.4 Check if sell actions fail when price of ticket is not within correct range >=10, <=100
    def test_ticket_price_invalid(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, price_too_low, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket price", "#sellErrorMessage")

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, price_too_high, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket price", "#sellErrorMessage")


    #R4.5 Check if sell actions fail when date is not in correct format
    def test_date_format_invalid(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, valid_price, date_non_numeric)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket expiry date", "#sellErrorMessage")

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, valid_price, date_from_the_past)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text("Invalid ticket expiry date", "#sellErrorMessage")


    #R4.6 Check if sell actions fail when business logic fails, and redirects to profile page with an error message
    @patch('qa327.backend.sell_ticket', return_value=sell_ticket_failure)
    def test_business_logic_failure(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, valid_price, valid_date)

        # Check that current page contains #sellErrorMessage
        self.assert_element("#sellErrorMessage")
        self.assert_text(sell_ticket_error_message, "#sellErrorMessage")

    #R4.7 Check if sell actions succeed with valid input and that new selling ticket information is posted on user profile page
    def test_sell_ticket_success(self, *_):
        # Start new session
        self.startNewSession()

        # Submit sell form
        self.submitSellForm(valid_ticket_name, valid_quantity, valid_price, valid_date)

        # Check that new selling ticket information is posted on user profile page
        self.assert_element("#tickets div h4")
        self.assert_text(valid_ticket_name + " " + str(valid_price), "#tickets div h4")
        self.assert_element("#tickets div h5")
        self.assert_text(str(valid_quantity) + " " + format_date(valid_date) + " " + valid_test_user_email, "#tickets div h5")