import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for R1

The tests will only test the frontend portion of the program, by patching the backend to return
specfic values. For example:

@patch('qa327.backend.get_user', return_value=test_user)

Will patch the backend get_user function (within the scope of the current test case)
so that it return 'test_user' instance below rather than reading
the user from the database.

Annotate @patch before unit tests can mock backend methods (for that testing function)
"""


class R1_2(BaseCase):

	def test_login_success(self, *_):
		"""
		This is a sample front end unit test to login to home page
		and verify if the tickets are correctly listed.
		"""
		# open login page
		self.open(base_url + '/login')
		# test if the page loads correctly
		self.assert_text("Please login", "#message")
