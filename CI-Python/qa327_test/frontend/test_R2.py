import pytest
from seleniumbase import BaseCase
from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from collections import namedtuple

######################################
# R2 Test Cases
# Checking all GET and POST requests for /register
######################################

#####
# Valid registration inputs
fields = namedtuple("fields", "email name password")
valid_fields = fields("test_frontend@test.com", "test frontend", "Valid123!")
# Valid User instance, matching valid_fields
valid_user = User(
    email='test_frontend@test.com',
    name='test frontend',
    password=generate_password_hash("Valid123!"),
    balance=5000
)
#####


@pytest.mark.usefixtures('server')
class TestRegistered(BaseCase):

    #######################
    # Helpful Functions
    #############
    # Opens /register page and attempts register POST with information from supplied User object
    def register_user(self, user):
        self.open(base_url + '/register')
        self.type("#email", user.email)
        self.type("#name", user.name)
        self.type("#password", user.password)
        self.type("#password2", user.password)
        return self.click('input[type="submit"]')

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

    ####################################################
    # R2 Test Cases
    #################################
    # GET requests
    #####################
    # R2.1 Check redirect to user profile page if already logged in
    @patch('qa327.backend.login_user', return_value=valid_user)
    @patch('qa327.backend.get_user', return_value=valid_user)
    def test_register_redirect(self, *_):
        # Invalidate any logged-in session
        self.logout()
        # Login user
        self.login(valid_fields)

        # GET request to /register
        self.get(base_url+'/register')
        # Check if we've been redirected to the home page
        self.assert_equal("Profile", self.get_title())

    #########
    # R2.2 Check if register.html renders on GET request if not already logged in
    def test_register_render(self):
        # Invalidate any logged-in session
        self.logout()

        # GET request to /register
        self.get(base_url+'/register')
        # Check that register.html renders by checking page title
        self.assert_equal("Register", self.get_title())

    #########
    # R2.3 Check the registration page shows form with appropriate fields
    def test_register_form_render(self):
        # Invalidate any logged-in session
        self.logout()

        # GET request to /register
        self.get(base_url+'/register')

        # Check if there is a form
        self.assert_element("form")

        # Check all required fields
        self.assert_element("input#email")
        self.assert_element("input#name")
        self.assert_element("input#password")
        self.assert_element("input#password2")

    #################################
    # POST requests
    #####################
    # R2.4 validate post req to /register
    def test_register_post(self):
        # Invalidate any logged-in session
        self.logout()

        # GET request to /register
        self.get(base_url + '/register')
        # Check if there is a form
        self.assert_element("form")
        # Check if form method is POST
        self.assertEqual("post", self.get_attribute("form", "method"))

    #########
    # R2.5 check all formatting reqs for email and password
    # Check if fields must be non-empty
    def test_form_not_empty(self):
        # Invalidate any logged-in session
        self.logout()

        # Check registering using empty email
        self.register_params("", valid_fields.name, valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        self.assert_equal("true", self.get_attribute("#email", "required"))     # Check if email is required

        # Check registering with empty password1
        self.register_params(valid_fields.email, valid_fields.name, "", valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        self.assert_equal("true", self.get_attribute("#name", "required"))  # Check if password1 is required

        # Check registering with empty password2
        self.register_params(valid_fields.email, valid_fields.name, valid_fields.password, "")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        self.assert_equal("true", self.get_attribute("#name", "required"))  # Check if password2 is required

    # Check if email must be addr-spec
    def test_email_valid(self):
        # Invalidate any logged-in session
        self.logout()

        # Check registering with non-addr-spec email string
        self.register_params("fake_email", valid_fields.name, valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("Email format error", "#message")

    # Check if password must meet strength requirements
    def test_password_valid(self):
        # Invalidate any logged-in session
        self.logout()

        # Password must be at least 6 characters
        self.register_params(valid_fields.email, valid_fields.name, "Pass!", "Pass!")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("Password not strong enough", "#message")

        # Password must contain at least one uppercase
        self.register_params(valid_fields.email, valid_fields.name, "passw!", "passw!")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("Password not strong enough", "#message")

        # Password must contain at least one lowercase
        self.register_params(valid_fields.email, valid_fields.name, "PASSW!", "PASSW!")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("Password not strong enough", "#message")

        # Password must contain at least one special character
        self.register_params(valid_fields.email, valid_fields.name, "Passwd", "Passwd")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("Password not strong enough", "#message")

    #########
    # R2.6 Check if both passwords must be the same
    def test_passwords_match(self):
        # Invalidate any logged-in session
        self.logout()

        # Try registering with two different passwords
        self.register_params(valid_fields.email, valid_fields.name, "Passwd1!", "Passwd2!")
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check error message
        self.assert_element("#message")
        self.assert_text("The passwords do not match", "#message")

    #########
    # R2.7 Username non-empty, alphanumeric with no leading or trailing spaces
    # Check if name must be non-empty
    def test_name_not_empty(self):
        # Invalidate any logged-in session
        self.logout()

        # Registering with empty name
        self.register_params(valid_fields.email, "", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        self.assert_equal("true", self.get_attribute("#name", "required"))  # Check name is required

    # Check if name must meet character specifications
    def test_name_valid(self):
        # Invalidate any logged-in session
        self.logout()

        # Registering name with leading spaces
        self.register_params(valid_fields.email, " test", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check for error message
        self.assert_element("#message")
        self.assert_text("Username format error", "#message")

        # Registering name with trailing spaces
        self.register_params(valid_fields.email, "test ", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check for error message
        self.assert_element("#message")
        self.assert_text("Username format error", "#message")

        # Registering name with special characters
        self.register_params(valid_fields.email, "!!!!!", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check for error message
        self.assert_element("#message")
        self.assert_text("Username format error", "#message")

    #########
    # R2.8 Check Username length
    def test_name_length(self):
        # Invalidate any logged-in session
        self.logout()

        # Try username too short
        self.register_params(valid_fields.email, " AB", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check for error message
        self.assert_element("#message")
        self.assert_text("Username format error", "#message")

        # Try username too long
        self.register_params(valid_fields.email, "anticonstitutionnell", valid_fields.password, valid_fields.password)
        self.assert_equal("Register", self.get_title())  # R2.9 stays on page for formatting error
        # Check for error message
        self.assert_element("#message")
        self.assert_text("Username format error", "#message")

    #########
    # R2.9 Refer to tests R2.5 through R2.8

    #########
    # R2.10 Show error message on registering with already used email
    @patch('qa327.backend.get_user', return_value=valid_user)
    def test_used_email(self, *_):
        # Invalidate any logged-in session
        self.logout()

        # Try to register same user as the one mocked in get_user
        self.register_user(valid_fields)
        self.assert_equal("Register", self.get_title())     # Stays on page
        # Check error message
        self.assert_element("#message")
        self.assert_text("This email has been ALREADY used", "#message")

    #########
    # R2.11 Valid inputs creates new user and redirects to /login
    @patch('qa327.backend.get_user', return_value=None)
    @patch('qa327.backend.register_user', return_value=None)
    def test_register_valid(self, *_):
        # Invalidate any logged-in session
        self.logout()

        # Register with valid registration inputs
        self.register_user(valid_fields)
        # Redirects to /login on successful register
        self.assert_equal("Log In", self.get_title())
