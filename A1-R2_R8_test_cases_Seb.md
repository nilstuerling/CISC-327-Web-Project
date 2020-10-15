
## R2 /register


*[GET]*

**R2.1.  If the user has logged in, redirect back to the user profile page /**

Mocking:

* Mock backend.get_user to return a test_user instance

Actions:

* Open /logout (to invalidate any logged-in sessions that may exist)
* Open /login
* Enter test_user’s email into element #email
* Enter test_user’s password into element #password
* Click element input[type=”submit”]
* Open /login
* Validate that the current page contains #welcome-header element (future implementation may not have a #welcome-header element)

**R2.2.  otherwise, show the user registration page**

Actions:

* Open /logout (to invalidate any logged-in sessions that may exist)
* Open /register
* Validate that the #register.html page renders

**R2.3.  the registration page shows a registration form requesting: email, user name, password, password2**

Actions:

* open /logout (to invalidate any logged-in sessions that may exist)
* open /register
* validate that the #register.html page renders and contains a form with input elements: #email, #user_name, #password and #password2
\
\
\
*[POST]*

**R2.4. The registration form can be submitted as a POST request to the current URL (/register)**

Actions:

* Open /logout (to invalidate any logged-in session that may exist)
* Open /register
* Enter valid email string that complies with addr-spec into element #email
* Enter valid user_name string into element #user_name
* Enter valid password string into element #password and #password2
* Validate that request type is POST (even if the strings entered in #password and #password2 do not match, a POST request should be emitted)

**R2.5. Email, password, password2 all have to satisfy the same required as defined in R1**

Actions:

* Open /logout (to invalidate any logged-in session that may exist)
* Open /register
* Leave element #email empty
* Enter valid user_name string into element #user_name
* Enter valid and matching password into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “Email format is incorrect. Empty email not allowed” and remains on register page
* Enter email string that does not comply with addr-spec into element #email
* Enter valid user_name string into element #user_name
* Enter valid and matching password into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “Email format is incorrect. Not a valid email” and remains on register page
* Enter non-empty email string that complies with addr-spec into element #email
* Enter valid user_name string into element #user_name
* Leave elements #password and #password2 empty
* Click element input[type=”submit”]
* Validate that page displays “Password format is incorrect. Empty password not allowed” and remains on register page
* Enter non-empty email string that complies with addr-spec into element #email
* Enter valid user_name string into element #user_name
* Enter matching 5 length string with uppercase, lowercase, and special character into elements #password and #password2
* Click element input[type="submit"]
* Validate that page displays “Password format is incorrect. Password needs to be: minimum length 6, have at least one upper case, at least one lower case, and at least one special character” and remains on register page
* Enter valid email string into element #email
* Enter valid user_name string into element #user_name
* Enter matching 6 length string with lowercase, special character, but no uppercase into elements #password and #password2
* Click element input[type="submit"]
* Validate that page displays “Password format is incorrect. Password needs to be: minimum length 6, have at least one upper case, at least one lower case, and at least one special character” and remains on register page
* Enter valid email string into element #email
* Enter valid user_name string into element #user_name
* Enter matching 6 length string with uppercase, special character, but no lowercase into elements #password and #password2
* Click element input[type="submit"]
* Validate that page displays “Password format is incorrect. Password needs to be: minimum length 6, have at least one upper case, at least one lower case, and at least one special character” and remains on register page
* Enter valid email string into element #email
* Enter valid user_name string into element #user_name
* Enter matching 6 length string with uppercase, lowercase, but no special character into elements #password and #password2
* Click element input[type="submit"]
* Validate that page displays “Password format is incorrect. Password needs to be: minimum length 6, have at least one upper case, at least one lower case, and at least one special character” and remains on register page

**R2.6.  Password and password2 have to be exactly the same**

Actions:

* Open /logout (to invalidate any logged-in sessions that may exist)
* Open /register
* Enter valid email string into element #email
* Enter valid user_name string into element #user_name
* Enter valid password string into element #password
* Enter valid password string, but different than the one entered into element #password, in element #password2
* Click element input[type=”submit”]
* Validate that page displays “Password format is incorrect. Passwords must match” and remains on register page

**R2.7.  User name has to be non-empty, alphanumeric-only, and space allowed only if it is not the first or the last character.**

Actions:

* Open /logout (to invalidate any logged-in sessions that may exist)
* Open /register
* Enter valid email string into element #email
* Leave element #user_name empty
* Enter valid and matching password string into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. Empty user name not allowed.” and remains on register page
* Enter valid email string into element #email
* Enter alphanumeric string, with a leading space character, into element #user_name
* Enter valid and matching password string into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. User name cannot contain leading spaces” and remains on register page
* Enter valid email string into element #email
* Enter alphanumeric string, with a trailing space character, into element #user_name
* Enter valid and matching password string into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. User name cannot contain trailing spaces” and remains on register page
* Enter valid email string into element #email
* Enter character “!!!!” into element #user_name
* Enter valid and matching password string into element #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. User name must be alphanumeric” and remains on register page

**R2.8.  User name has to be longer than 2 characters and less than 20 characters.**

Actions:

* Open /logout (to invalidate any logged-in sessions)
* Open /register
* Enter valid email string into element #email
* Enter string “AB” into element #user_name
* Enter valid and matching password in elements #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. User name too short: must be between 3 and 19 characters” and remains on register page
* Enter valid email string into element #email
* Enter alphanumeric string, with no spaces, of length 20 into element #user_name
* Enter valid and matching password in elements #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “User name format is incorrect. User name too long: must be between 3 and 19 characters” and remains on register page

**R2.10.  If the email already exists, show message 'this email has been ALREADY used'**

Mocking:

* Mock backend.get_user to return a valid_user instance

Actions:

* Open /logout (to invalidate any logged-in sessions)
* Open /register
* Enter test_user’s email into the element #email
* Enter valid user_name string into element #user_name
* Enter valid and matching passwords into elements #password and #password2
* Click element input[type=”submit”]
* Validate that page displays “This email has been ALREADY used” and remains on register page

**R2.11. If no error regarding the inputs following the rules above, create a new user, set the balance to 5000, and go back to the /login page**

Actions:

* Open /logout (to invalidate any logged-in sessions)
* Open /register
* Enter valid and unused email string in the element #email
* Enter a valid user_name string in element #user_name
* Enter valid and matching password in elements #password and #password2
* Click element input[type=”submit”]
* Validate that a new user has been created, user information matching the input fields and account balance at 5000 (can be done by querying database by email, then validating user fields)
* Validate that the #login.html page renders

## R8 /*

*[any]*

**R8.1 For any other requests except the ones above, the system should return a 404 error**

Actions

* Open /*, with * corresponding to any non-empty string except for “login”, “register”, “sell”, “update”, “buy”, and “logout”
* Validate that an error 404 is returned