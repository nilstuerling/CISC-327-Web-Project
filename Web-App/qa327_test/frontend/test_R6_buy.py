import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Tickets
from werkzeug.security import generate_password_hash, check_password_hash

# Mock valid email and password for user
valid_test_user_email="test_frontend@test.com"
valid_test_user_password="Test_frontend!"

# Mock a sample user
test_user = User(
    id = 1,
    email=valid_test_user_email,
    name='test_frontend',
    password=generate_password_hash(valid_test_user_password),
    balance = 101
)

# Mock no user returned
no_user = None

# Mock some sample tickets
test_tickets = [
    Tickets(email='test_frontend@test.com',name="t1",date='24/12/2020',quantity=3,price=15),
    Tickets(email='test_frontend@test.com',name="t2",date='24/12/2020',quantity=3,price=70)
]


# set balance to 101

# not enough balance
#   try to purchase quantity: 2 of ticket2 - check that this returns error
#   try to purchase quantity: 1 of ticket2 - check that this goes through



@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.get_all_tickets', return_value=test_tickets)
class Test_R6(BaseCase):

    # helper functions
    def login(self):
        self.open(base_url + '/login')
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)
        return self.click('input[type="submit"]')

    def logout(self):
        self.get(base_url + '/logout')


    def start_new_session(self):
        self.logout()
        self.login()
        self.assert_element("#welcome-header")

    def submitBuyForm(self, name, quantity):
        self.type("#buyName", name)
        self.type("#buyQuantity", quantity)
        return self.click('input[id="btn-submit2"]')



    # R6.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character
    def test_ticket_name(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # empty name
        self.submitBuyForm("",  "")
        self.get_attribute("#buyName", "required")
        self.assert_element("#welcome-header") # stays on main page

        # space at front
        self.submitBuyForm(" ticketTest",  "1")
        self.assert_text("Invalid ticket name","#buyErrorMessage")
        self.assert_element("#welcome-header") # stays on main page

        # space at end
        self.submitBuyForm("ticketTest ",  "1")
        self.assert_text("Invalid ticket name","#buyErrorMessage") # stays on main page
        self.assert_element("#welcome-header") # stays on main page

        # special character
        self.submitBuyForm("ticket$Test",  "1")
        self.assert_text("Invalid ticket name","#buyErrorMessage") # stays on main page
        self.assert_element("#welcome-header") # stays on main page

        # passing ticket
        self.submitBuyForm("t1",  "1")
        self.assert_text("","#buyErrorMessage") # stays on main page
        self.assert_element("#welcome-header") # stays on main page


    # R6.2 - The name of the ticket is no longer than 60 characters
    def test_ticket_name_length(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # empty name
        self.submitBuyForm("",  "1")
        self.get_attribute("#buyName", "required")
        self.assert_element("#welcome-header") # stays on main page

        # too long name
        self.submitBuyForm("reallyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyylongname",  "1")
        self.assert_text("Invalid ticket name","#buyErrorMessage")
        self.assert_element("#welcome-header")

        # passing ticket
        self.submitBuyForm("t1",  "1")
        self.assert_text("","#buyErrorMessage") # stays on main page
        self.assert_element("#welcome-header") # stays on main page


    # R6.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100
    def test_ticket_quantity_bounds(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # empty quantity
        self.submitBuyForm("ticketTest",  "")
        self.get_attribute("#buyQuantity", "required")
        self.assert_element("#welcome-header") # stays on main page

        # too little
        self.submitBuyForm("t1",  "0")
        self.assert_text("Invalid ticket quantity","#buyErrorMessage")
        self.assert_element("#welcome-header")

        # too much
        self.submitBuyForm("t1",  "101")
        self.assert_text("Invalid ticket quantity","#buyErrorMessage")
        self.assert_element("#welcome-header")

        # passing
        self.submitBuyForm("t1",  "2")
        self.assert_text("","#buyErrorMessage")
        self.assert_element("#welcome-header")


    # R6.4 - The ticket name exists in the database and the quantity is more than the quantity requested to buy
    @patch('qa327.backend.buy_ticket', return_value="Invalid Ticket Quantity")
    def test_ticket_name_exists(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # invalid ticket name
        self.submitBuyForm("t0", "2")
        self.assert_text("Invalid ticket name: ticket does not exist", "#buyErrorMessage")

        # valid ticket name
        self.submitBuyForm("t1", "2")
        self.assert_text("", "#buyErrorMessage")


    def test_enough_quantity_to_purchase(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # valid ticket name but too much requested
        self.submitBuyForm("t1",  "4")
        self.assert_text("Invalid Ticket Quantity", "#buyErrorMessage")

        # valid ticket name and valid amount
        self.submitBuyForm("t1", "1")
        self.assert_text("", "#buyErrorMessage")

        
    # R6.5 - The user has more balance than the ticket price * quantity + service fee (35%) + tax (5%)
    @patch('qa327.backend.buy_ticket', return_value="Invalid purchase order: insufficient funds")
    def test_user_enough_balance(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        # valid name and valid quantity, but not enough balance
        self.submitBuyForm("t2", "2")
        self.assert_text("Invalid purchase order: insufficient funds", "#buyErrorMessage")

        # valid name, quantity and balance
        self.submitBuyForm("t2", "1")
        self.assert_text("", "#buyErrorMessage")


    # R6.6 - For any errors, redirect back to / and show an error message
    def test_general_errors(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        


