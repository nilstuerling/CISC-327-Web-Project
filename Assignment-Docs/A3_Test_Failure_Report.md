## Assignment 3 - Failure Report:

### Template Changes

Added *db.drop_all()* to the database so that on startup, a fresh database is created each time. This helped rectify some issues we were having with previously created data, and also allowed for safer live testing. Alternative solutions may be reviewed in the future in order to allow persistent data between server starts.

### R1 Frontend Failure Report

**R1.3** - Fixed implementation in frontend logic for GET request to /login to redirect to user profile page if "logged_in" was in the current session

**R1.6** - Test case different from its respective test spec in R1 requirements document. Checking for non-empty inputs is done by ensuring that the form elements _#email_ and _#password_ have the _required_ attribute, thereby ensuring that input cannot be empty.

**R1.8** - Fixed implementation for password validation in logic due to test case. Test case did not fail on case where password was missing a special character. Backend logic fixed to return an invalid password response on this condition (previous logic was not checking for special characters properly).

**R1.9** – To clarify, the error message response for this requirement was used in all previous formatting errors. Each of the previous formatting errors checks for this error message response.

**R1.11** – Test case different from its respective test spec in R1 requirements document. No need to enter invalid user&#39;s credentials, instead the test just mocks an invalid return from the database.

<br>

### R2 Frontend Failure Report

**All Test Cases** - Changed name "test_user" to "valid_user"

**R2.1** - Failing a conditional inside wrapper function frontend.authenticate, and redirecting to logout instead
* Fixed by mocking backend.login_user to return valid_user instance
* Also added similar frontend.authenticate-like functionality in frontend '/register' GET method, to not only 
    check if user is logged in but if user exists

**R2.2** - Could not directly validate an html page rendering with Seleniumbase
* Fixed by validating current source page has title "Register" (as in register.html)

**R2.5** - POST request not processed when form fields left empty, and could not check error message
* Fixed by checking if form input has attribute "required"
* Changed order of tests so all non-empty checks are first
* Error message formatting does not fully match (eg "Email format
is incorrect" instead of "Email format is incorrect: Must be a valid email address")
* Simplified test case error message, as in original requirements
* Registration attempt with password with no special character fails error message check
* Fixed boolean condition in backend.validatePassword

**R2.7** - POST request not processed when form fields left empty, and could not check error message
* Fixed by checking if form input has attribute "required"
    
**R2.11** - No methods to access database and check user account balance
* Migrating user account balance requirement check to backend testing
* Deferring account balance test for now, just checking successful register and redirect to /login
* Mocked backend.get_user to return None, so we pass the check if email has already been used
* Mocked backend.register_user to avoid adding user in database while registering

<br>

### R3 Frontend Failure Report:

**R3 All** - Error in testing caused by unpatched server and backend. Fixed by patching up the backend and returning a fixed response to test the frontend part of the application.

**R3.5** - Fixed the expired sort feature within the frontend file. Now it works with a list of dictionaries, and filters out all the expired tickets. 

**R3.6** - Fixed the sell feature in the frontend file. Now message is displayed when a ticket is successfully added to the ticket database else displays error message. 

**R3.7** - Fixed the buy feature in the frontend file. Now message is displayed when a ticket is sold successfully else prints error message. 

**R3.8** - Fixed the update feature in the frontend file. Now message is displayed when a ticket is successfully updated else prints error message.

**R3.9 & R3.10 & R3.10 & R3.11** - Test case was unable to differentiate between the different forms on the / page. This was fixed by adding an action attribute to each on of the sell form, buy form and update form. The test case was then changed to assert if the action was correct and redirected to their dedicated pages and if the method, being post, was correct on all forms. This resolved the issue. 

<br>

### R7 Frontend Failure Report

**R7.1** - Opening endpoints for ticket transactions (`/buy`, `/sell`, `/update`) in the browser (this would be GET request) resulted in an internal error and a response to the user saying the method is not available
* Fixed by adding the proper methods to implement GET requests to said endpoints. It redirects to `/` if they are logged in, thus taking them to their userpage where they can properly interact with buying, selling, and updating tickets. If they are not logged in, it redirects to `/login`, where they can either login or register.

* Making POST requests to endpoints for ticket transactions (`/buy`, `/sell`, `/update`) while not logged in resulted in an error
  * Fixed by adding a check to make sure the user was logged in. If they are not, it redirects them to `/login`, where they can login or register. If they are, it continues with the rest of the action as normal.

<br>

### R8 Frontend Failure Report

**R8.1** - No errors occurred; however, added an `id="response"` to the 404 template page to better check for the 404 response.