import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User, Tickets
from werkzeug.security import generate_password_hash, check_password_hash


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

# Mock some sample tickets
test_tickets = [Tickets(email='test_frontend@test.com',name="t1",date='24/12/2020',quantity='1',price='100')]

@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.get_all_tickets', return_value=test_tickets)
class test_R5(BaseCase):

	# R3.1 - Checks that if the user is not logged in, redirect to login page
	def test_validate_TicketName(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		self.type("#updateName", " testTitle")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

		self.type("#updateName", "testTitle ")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

		self.type("#updateName", "testTitle.")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")


	def test_validate_length_TicketName(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		self.type("#updateName", "HelloThereThisIsATestOfHowManyCharactersFitIntoATicketNameGoodbye")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")


	def test_validate_TicketQuantity(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		self.type("#updateName", "t1")
		self.type("#updateQuantity", "0")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket quantity", "#updateErrorMessage")

		self.type("#updateName", "t1")
		self.type("#updateQuantity", "101")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket quantity", "#updateErrorMessage")


	def test_validate_TicketPrice(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "9")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket price", "#updateErrorMessage")

		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "101")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket price", "#updateErrorMessage")


	def test_validate_TicketExists(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		self.type("#updateName", "testTicket")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "9")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name: does not exist", "#updateErrorMessage")
