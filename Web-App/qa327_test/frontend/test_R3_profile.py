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
class test_R3(BaseCase):

	# R3.1 - Checks that if the user is not logged in, redirect to login page
	def test_not_logged_in_redirect_to_login_page(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open homepage while not logged in
		self.open(base_url + '/')

		# Test if login.html template was rendered by checking if "Log In" header exists
		self.assert_element("h1")
		self.assert_text("Log In", "h1")

	# R3.2 - Checks if this page shows a header 'Hi {}'.format(user.name)
	def test_this_page_header(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Check that the homepage greets the user with 'Hi {}'.format(user.name)
		self.assert_text("Hi test_frontend", "#welcome-header")

	# R3.3 - Checks if this page shows user balance.
	def test_this_page_user_balance(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Check if the user balance exists and shows the correct amount
		self.assert_element("#user_balance")
		self.assert_text("5000", "#user_balance")

	# R3.4 - Checks if this page shows a logout link, pointing to /logout
	def test_this_page_logout_link(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Check if there exists a log out link on the homepage (the / page)
		self.assert_element("#logout_link")

	# R3.5 - Checks if This page lists all available tickets.
	# Information including the quantity of each ticket, the owner's email, and the price,
	# for tickets that are not expired.
	def test_this_page_all_tickets(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that all tickets are displayed correctly on the homepage
		ticket_np = self.find_elements("#tickets div h4")
		assert any("t1" in el.text and str(100) in el.text for el in ticket_np)

		ticket_dqe = self.find_elements("#tickets div h5")
		assert any("24/12/2020" in el.text and str(1) in el.text and "test_frontend@test.com" in el.text for el in ticket_dqe)

	# R3.6 - Checks if this page contains a form that a user can submit new tickets for sell.
	# Fields: name, quantity, price, expiration date
	def test_this_page_sell_tickets(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that there exists a sell form with the fields: name, quantity, price, expiration date
		self.assert_element("#name")
		self.assert_element("#quantity")
		self.assert_element("#price")
		self.assert_element("#expireDate")

	# R3.7 - Checks if this page contains a form that a user can buy new tickets. Fields: name, quantity
	def test_this_page_buy_tickets(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that there exists a buy form with the fields: name, quantity
		self.assert_element("#buyName")
		self.assert_element("#buyQuantity")

	# R3.8 - Checks if this page contains a form that a user can update existing tickets.
	# Fields: name, quantity, price, expiration date
	def test_this_page_update_tickets(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that there exists an update form with the fields: name, quantity, price, expiration date
		self.assert_element("#updateName")
		self.assert_element("#updateQuantity")
		self.assert_element("#updatePrice")
		self.assert_element("#updateExpireDate")

	# R3.9 - Checks if ticket-sell can be posted to /sell
	def test_this_page_redirect_to_sell(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that the post method and the /sell action have been conducted correctly and redirected the user to /sell
		self.assertEqual("post", self.get_attribute("form[id='sellTicket']", "method"))
		self.assertEqual(base_url + '/sell', self.get_attribute("form[id='sellTicket']", "action"))

	# R3.10 - Checks if ticket-buy can be posted to /buy
	def test_this_page_redirect_to_buy(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that the post method and the /buy action have been conducted correctly and redirected the user to /buy
		self.assertEqual("post", self.get_attribute("form[id='buyTicket']", "method"))
		self.assertEqual(base_url + '/buy', self.get_attribute("form[id='buyTicket']", "action"))

	# R3.11 - Checks if ticket-update can be posted to /update
	def test_this_page_redirect_to_update(self, *_):
		# Open logout page, invalid any logged-in sessions that may exist
		self.open(base_url + '/logout')

		# Open login page
		self.open(base_url + '/login')

		# Fill email and password
		self.type("#email", valid_test_user_email)
		self.type("#password", valid_test_user_password)

		# Click submit button
		self.click('input[type="submit"]')

		# Test that current page contains #welcome-header (i.e. redirected to user profile page)
		self.assert_element("#welcome-header")

		# Checks that the post method and the /update action have been conducted correctly and redirected the user to /update
		self.assertEqual("post", self.get_attribute("form[id='updateTicket']", "method"))
		self.assertEqual(base_url + '/update', self.get_attribute("form[id='updateTicket']", "action"))
