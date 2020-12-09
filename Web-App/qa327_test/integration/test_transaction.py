import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple


# Valid registration inputs
regFields = namedtuple("regFields", "email name password")
user1 = regFields("user1@test.com", "user1", "Valid123!")
user2 = regFields("user2@test.com", "user2", "Valid123!")

ticketFields = namedtuple("ticketFields", "name date quantity price")
tix = ticketFields("Dream Theater Metropolis Pt 2 Scenes From a Memory", "20210420", 20, 50)


@pytest.mark.usefixtures('server')
class TestSellPath(BaseCase):

    #######################
    # Helpful Functions
    #############
    # Opens /register page and attempts register POST with supplied parameters
    def register_params(self, email, name, password1, password2):
        self.open(base_url + '/register')
        self.type("#email", email)
        self.type("#name", name)
        self.type("#password", password1)
        self.type("#password2", password2)
        return self.click('input[type="submit"]')

    # Opens /login and attempts login POST with information from supplied User object
    def login(self, user):
        self.open(base_url + '/login')
        self.type("#email", user.email)
        self.type("#password", user.password)
        return self.click('input[type="submit"]')

    # Gets /logout and logs out current user if any
    def logout(self):
        self.get(base_url + '/logout')



    def test_selling_path(self):
        self.logout()
        self.register_params(user1.email, user1.name, user1.password, user1.password)
        self.login(user1)

        self.type("#name", tix.name)
        self.type("#quantity", tix.quantity)
        self.type("#price", tix.price)
        self.type("#expireDate", tix.date)


