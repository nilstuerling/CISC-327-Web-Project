import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Mock a sample user
test_user = User(
	email='test_frontend@test.com',
	name='test_frontend',
	password='test_frontend'
)

class FrontEndLogoutTest(BaseCase):

	@patch('qa327.backend.get_user', return_value=test_user)
	def test_login_success(self, *_):
		# remove any current sessions
		self.open(base_url + '/logout')

		# create a session
		self.open(base_url + '/login')
		self.type("#email", test_user.email)
		self.type("#password", test_user.password)
		self.click('input[type="submit"]')

		# logout of session
		self.open(base_url + '/logout')

		# verify that we have closed session/logged out
		# open root url, this should redirect to login
		self.open(base_url + '/')
		self.assert_text("Please login", "#message")

		# open root buy page, this should redirect to login
		self.open(base_url + '/buy')
		self.assert_text("Please login", "#message")

		# open root sell page, this should redirect to login
		self.open(base_url + '/sell')
		self.assert_text("Please login", "#message")

		# open root update page, this should redirect to login
		self.open(base_url + '/update')
		self.assert_text("Please login", "#message")




