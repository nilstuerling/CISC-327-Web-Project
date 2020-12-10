import pytest
from seleniumbase import BaseCase

from qa327_test.conftest import base_url
from unittest.mock import patch
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

"""
This file defines all unit tests for the /login endpoint.

The tests will only test the frontend portion of the /login endpoint, and will patch the backend to return specific values for different test cases
"""

# Mock valid email and password for user
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

# Mock no user returned
no_user = None

class FrontEndLoginPageTest(BaseCase):

    # R1.1 - If the user hasn't logged in, show the login page
    def test_display_login(self):
        
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Test if login.html template was rendered by checking if "Log In" header exists
        self.assert_element("h1")
        self.assert_text("Log In", "h1")
    
    # R1.2 - The login page has a message that by default says 'please login'
    def test_login_page_default_message(self):

        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Test that login page contains #message element with message "Please login"
        self.assert_element("#message")
        self.assert_text("Please login", "#message")

    # R1.3 - If the user has logged in, redirect to the user profile page
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_logged_in_redirect_to_user_profile(self, *_):

        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email and password
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)

        # Click submit button
        self.click('input[type="submit"]')

        # Open login page again
        self.open(base_url + '/login')

        # Test that current page contains #welcome-header (i.e. redirected to user profile page)
        self.assert_element("#welcome-header")

    # R1.4 - The login page provides a login form which requests two fields: email and passwords
    def test_login_page_form(self):
        
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Test if login.html template was rendered by checking if "Log In" header exists
        self.assert_element("h1")
        self.assert_text("Log In", "h1")

        # Test login page contains form elements #email and #password
        self.assert_element("#email")
        self.assert_element("#password")

    # R1.5 - The login form can be submitted as a POST request to the current URL (/login)
    def test_login_post_request(self):
                 
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')
        
        # Test that there exists a form with method POST
        self.assert_element("form")
        method = self.get_attribute("form", "method")
        self.assertEqual("post", method)

    # R1.6 - Email and password both cannot be empty
    def test_email_password_not_empty(self):
                         
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email with empty string
        self.type("#email", "")
        # Fill password with valid password
        self.type("#password", valid_test_user_password)

        # Click submit button
        self.click('input[type="submit"]')

        # Test that #email form element has attribute "required" (not allowing empty input)
        self.get_attribute("#email", "required")

        # Attempt second login
        self.open(base_url + '/login')

        # Fill email with valid email
        self.type("#email", valid_test_user_email)
        # Fill password with empty string
        self.type("#password", "")

        # Click submit button
        self.click('input[type="submit"]')

        # Test that #password form element has attribute "required" (not allowing empty input)
        self.get_attribute("#password", "required")

    # R1.7 - Email has to follow addr-spec defined in RFC 5322
    def test_email_valid(self):
                                 
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email with invalid email
        self.type("#email", "randomemail.com")
        # Fill password with valid password
        self.type("#password", valid_test_user_password)

        # Click submit button
        self.click('input[type="submit"]')

        # Test that login page contains #message element with error message
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")

    # R1.8 - Password has to meet the required complexity: minimum length 6, at least one upper case, at least one lower case, and at least one special character
    def test_password_valid(self):
                                         
        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email with email
        self.type("#email", valid_test_user_email)
        # Fill password with invalid password (too short, needs at least 6 characters)
        self.type("#password", "Pass!")

        # Click submit button
        self.click('input[type="submit"]')

        # Test that login page contains #message element with error message
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


        # Fill email with valid email
        self.type("#email", valid_test_user_email)
        # Fill password with invalid password (no uppercase)
        self.type("#password", "passw!")

        # Click submit button
        self.click('input[type="submit"]')

        # Test that login page contains #message element with error message
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


        # Fill email with valid email
        self.type("#email", valid_test_user_email)
        # Fill password with invalid password (no lowercase)
        self.type("#password", "PASSW!")

        # Click submit button
        self.click('input[type="submit"]')

        # Test that login page contains #message element with error message
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


        # Fill email with valid email
        self.type("#email", valid_test_user_email)
        # Fill password with invalid password (no special character)
        self.type("#password", "Passwd")

        # Click submit button
        self.click('input[type="submit"]')

        # Test that login page contains #message element with error message
        self.assert_element("#message")
        self.assert_text("Email/Password format is incorrect", "#message")


    # R1.9 - If email/password are correct, redirect to /
    @patch('qa327.backend.login_user', return_value=test_user)
    @patch('qa327.backend.get_user', return_value=test_user)
    def test_valid_email_password_login_success(self, *_):

        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email and password
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)

        # Click submit button
        self.click('input[type="submit"]')

        # Test that current page contains #welcome-header element (i.e. on user profile page)
        self.assert_element("#welcome-header")

    # R1.9 - If email/password are incorrect redirect to /login and show message 'Email/Password combination incorrect'
    @patch('qa327.backend.login_user', return_value=no_user)
    def test_valid_email_password_login_fail(self, *_):

        # Open logout page, invalid any logged-in sessions that may exist
        self.open(base_url + '/logout')
        
        # Open login page
        self.open(base_url + '/login')

        # Fill email and password
        self.type("#email", valid_test_user_email)
        self.type("#password", valid_test_user_password)

        # Click submit button
        self.click('input[type="submit"]')

        # Test that current page is login page with correct error message
        self.assert_element("#message")
        self.assert_text("Email/Password combination incorrect", "#message")
