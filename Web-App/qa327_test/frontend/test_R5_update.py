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
test_tickets = [Tickets(email='test_frontend@test.com',name="t1",date='20201224',quantity='1',price='100')]

@patch('qa327.backend.get_user', return_value=test_user)
@patch('qa327.backend.get_all_tickets', return_value=test_tickets)
class test_R5(BaseCase):

	# R5.1 - The name of the ticket has to be alphanumeric-only, and space allowed only if it is not the first or the last character.
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

		#test false ticket name with space at front
		self.type("#updateName", " testTitle")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

		#test false ticket name with space as last element
		self.type("#updateName", "testTitle ")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

		#test false ticket name with special character and not just alphanumeric characters
		self.type("#updateName", "testTitle.")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

	#R5.2 - The name of the ticket is no longer than 60 characters
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

		#test ticket length with length longer than 60 characters
		self.type("#updateName", "HelloThereThisIsATestOfHowManyCharactersFitIntoATicketNameGoodbye")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name", "#updateErrorMessage")

	#R5.3 - The quantity of the tickets has to be more than 0, and less than or equal to 100.
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

		#test quantity with too low quantity
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "0")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket quantity", "#updateErrorMessage")

		#test quanity with too high quantity
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "101")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket quantity", "#updateErrorMessage")

	#R5.4 - Price has to be of range [10, 100]
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

		#test price with too low price
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "9")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket price", "#updateErrorMessage")

		#test price with too high price
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "101")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket price", "#updateErrorMessage")

	#R5.5 - Date must be given in the format YYYYMMDD (e.g. 20200901)
	def test_validate_TicketDate(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		#test date with date in wrong format
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "24/12/2020")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket expiry date", "#updateErrorMessage")

		#test date with expired date
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20191210")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket expiry date", "#updateErrorMessage")

	#R5.6 - The ticket of the given name must exist
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

		#test that ticket exists with false ticket name
		self.type("#updateName", "testTicket")
		self.type("#updateQuantity", "1")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")
		self.assert_text("Invalid ticket name: does not exist", "#updateErrorMessage")

	#R5.7 - For any errors, redirect back to / and show an error message
	def test_validate_redirect_to_home(self, *_):
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

		#test error message with false quantity
		self.type("#updateName", "t1")
		self.type("#updateQuantity", "101")
		self.type("#updatePrice", "100")
		self.type("#updateExpireDate", "20201224")
		self.click("input[id='btn-submit3']")

		#verify that after fasle submission, user is redirected back to /
		self.assert_element("#welcome-header")
		self.assert_element("#updateErrorMessage")
		self.assert_text("Invalid ticket quantity", "#updateErrorMessage")
