import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple


# Valid registration inputs
regFields = namedtuple("regFields", "email name password")
user1 = regFields("user1@test.com", "user1", "Valid123!")
user2 = regFields("user2@test.com", "user2", "Valid123!")

ticketFields = namedtuple("ticketFields", "name date quantity price email")
tix = ticketFields("Dream Theater Metropolis Pt 2 Scenes From a Memory", "20210420", "20", "50", user1.email)


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

    # Formats date from string input into printable string
    def format_date(self, date):
        return date[6:] + "/" + date[4:6] + "/" + date[0:4]

    # Opens user profile and attempts /sell POST with supplied ticket information
    def sell_tix(self, tix):
        self.open(base_url + "/")
        self.type("#name", tix.name)
        self.type("#quantity", tix.quantity)
        self.type("#price", tix.price)
        self.type("#expireDate", tix.date)
        self.click("#btn-submit")


    def test_1selling_path(self):
        self.logout()
        self.register_params(user1.email, user1.name, user1.password, user1.password)
        self.login(user1)

        self.sell_tix(tix)

        ticket_NamePrices = self.find_elements("#tickets div h4")
        assert any(tix.name in el.text and tix.price in el.text for el in ticket_NamePrices)

        ticket_DateQuantityEmail = self.find_elements("#tickets div h5")
        assert any(self.format_date(tix.date) in el.text and tix.quantity in el.text and tix.email in el.text
                   for el in ticket_DateQuantityEmail)


    def test_2buying_path(self):
        # Sell a ticket with a first user, so we may have a ticket listing
        self.logout()
        self.register_params(user1.email, user1.name, user1.password, user1.password)
        self.login(user1)
        self.sell_tix(tix)

        # Log in as a second user to buy tickets
        self.logout()
        self.register_params(user2.email, user2.name, user2.password, user2.password)
        self.login(user2)

        # Check there are tickets available for purchase
        ticket_NamePrices = self.find_elements("#tickets div h4")
        assert any(tix.name in el.text and tix.price in el.text for el in ticket_NamePrices)

        # Buy all available tickets
        self.type("#buyName", tix.name)
        self.type("#buyQuantity", tix.quantity)
        self.click("#btn-submit2")

        # Assert the tickets we just bought got unlisted
        ticket_NamePrices = self.find_elements("#tickets div h4")
        assert not any(tix.name in el.text and tix.price in el.text for el in ticket_NamePrices)






