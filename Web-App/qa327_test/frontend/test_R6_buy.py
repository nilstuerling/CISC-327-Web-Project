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
    Tickets(email='test_frontend@test.com',name="t1",date='20201224',quantity='3',price='15'),
    Tickets(email='test_frontend@test.com',name="t2",date='20201224',quantity='3',price='75')
]


# have two tickets in the system
#   ticket1 in system should be of price 15 and quantity 3;
#   ticket2 in system should be of price 75 and quantity 3;


# set balance to 101

# not enough quantity
#   try to purchase quantity: 4 of ticket1 - check that this returns error
#   try to purhcase quantity: 3 of ticket1 - check that this goes through


# not enough balance
#   try to purchase quantity: 2 of ticket2 - check that this returns error
#   try to purchase quantity: 1 of ticket2 - check that this goes through



@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.get_all_tickets', return_value=test_tickets)
class FrontEndBuy(BaseCase):
    def login(self):
        self.open(base_url + '/login')
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)
        return self.click('input[type="submit"]')

    # Gets /logout and logs out current user if any
    def logout(self):
        self.get(base_url + '/logout')


    def start_new_session(self):
        self.logout()
        self.login()
        self.assert_element("#welcome-header")

    def test_enough_quantity_to_purchase(self, *_):
        self.start_new_session()
        self.open(base_url + '/')

        self.assert_text("no text", "h2")

        

