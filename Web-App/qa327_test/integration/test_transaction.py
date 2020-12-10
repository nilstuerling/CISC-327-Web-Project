import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple
from decimal import Decimal


# Valid registration inputs
regFields = namedtuple("regFields", "email name password")
user1 = regFields("user1@test.com", "user1", "Valid123!")
user2 = regFields("user2@test.com", "user2", "Valid123!")

# Valid ticket arguments
ticketFields = namedtuple("ticketFields", "name date quantity price email")
tix = ticketFields("Dream Theater Metropolis Pt 2 Scenes From a Memory", "20210420", "20", "50", user1.email)
tix2 = ticketFields("blankName", "20220101", "40", "20", user1.email)

@pytest.mark.usefixtures('fresh_server')
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

    # Opens user profile and attempts /sell POST with supplied ticket information
    def sell_tix(self, tix):
        self.open(base_url + "/")
        self.type("#name", tix.name)
        self.type("#quantity", tix.quantity)
        self.type("#price", tix.price)
        self.type("#expireDate", tix.date)
        self.click("#btn-submit")

    # Formats date from string input into printable string
    def format_date(self, date):
        return date[6:] + "/" + date[4:6] + "/" + date[0:4]

    # Returns total price from ticket quantity and price
    def get_total_price(self, quantity, price):
        return Decimal(((quantity * price) * 1.35) * 1.05)  # service fee: 1.35 (35%), tax: 1.05 (5%)
    #########################
    # INTEGRATION TESTING

    # User registration to ticket selling path
    def test_selling_path(self):
        # Register and login a new user
        self.logout()
        self.register_params(user1.email, user1.name, user1.password, user1.password)
        self.login(user1)

        # Attempt ticket selling
        self.sell_tix(tix)

        # Validate ticket we just sold is listed
        ticket_NamePrices = self.find_elements("#tickets div h4")
        assert any(tix.name in el.text and tix.price in el.text for el in ticket_NamePrices)

        ticket_DateQuantityEmail = self.find_elements("#tickets div h5")
        assert any(self.format_date(tix.date) in el.text and tix.quantity in el.text and tix.email in el.text
                   for el in ticket_DateQuantityEmail)

    # User registration to ticket updating path
    def test_updating_path(self):
        # Sell a ticket first, so we may have a ticket listing
        self.logout()
        self.register_params(user1.email, user1.name, user1.password, user1.password)
        self.login(user1)
        self.sell_tix(tix)

        # Enter name of ticket we just sold, so we update it
        self.type("#updateName", tix.name)
        # Enter and submit updated fields
        self.type("#updateQuantity", tix2.quantity)
        self.type("#updatePrice", tix2.price)
        self.type("#updateExpireDate", tix2.date)
        self.click("#btn-submit3")

        # Validate ticket has been updated to new values
        ticket_NamePrices = self.find_elements("#tickets div h4")
        assert any(tix.name in el.text and tix2.price in el.text for el in ticket_NamePrices)

        ticket_DateQuantityEmail = self.find_elements("#tickets div h5")
        assert any(self.format_date(tix2.date) in el.text and tix2.quantity in el.text and tix.email in el.text
                   for el in ticket_DateQuantityEmail)

    # User registration to ticket buying path
    def test_buying_path(self):
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

        # Assert the user balance has been adjusted accordingly
        assert str(5000 - self.get_total_price(int(tix.quantity), int(tix.price))) \
               in self.find_element("#user_balance").text







