import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash




class R8_1(BaseCase):
	def test_404(self, *_):
		"""
		This is a sample front end unit test to login to home page
		and verify if the tickets are correctly listed.
		"""
		# open a nonexistant page
		self.open(base_url + '/nonsense')

		# verify response code and 404 text
                # response code
		self.assert_text("404", "#response")
