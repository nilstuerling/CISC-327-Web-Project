import pytest

from qa327.backend import validateEmail
from qa327.backend import validatePassword

valid_email = "valid_email@gmail.com"
invalid_email = "invalidemail.com"

def test_valid_email():
    assert validateEmail(valid_email) == True

def test_invalid_email():
    assert validateEmail(invalid_email) == False



too_short_password = "nope!"
no_upper_password = "password!"
no_lower_password = "PASSWORD!"
no_special_password = "Password"
valid_password = "Password!"

def test_password_too_short():
    assert validatePassword(too_short_password) == False

def test_password_no_uppercase():
    assert validatePassword(no_upper_password) == False

def test_password_no_lowercase():
    assert validatePassword(no_lower_password) == False

def test_password_no_special_character():
    assert validatePassword(no_special_password) == False

def test_valid_password():
    assert validatePassword(valid_password) == True

