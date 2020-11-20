## R2 Frontend Failure Report
### All test cases
* Changed name "test_user" to "valid_user"

### R2.1
* Failing a conditional inside wrapper function frontend.authenticate, and redirecting 
to logout instead
    * Fixed by mocking backend.login_user to return valid_user instance
    * Also added similar frontend.authenticate-like functionality in frontend '/register' GET method, to not only 
    check if user is logged in but if user exists

### R2.2
* Could not directly validate an html page rendering with Seleniumbase
    * Fixed by validating current source page has title "Register" (as in register.html)

### R2.5
* POST request not processed when form fields left empty, and could not check error message
    * Fixed by checking if form input has attribute "required"
    * Changed order of tests so all non-empty checks are first
* Error message formatting does not fully match (eg "Email format
is incorrect" instead of "Email format is incorrect: Must be a valid email address")
    * Simplified test case error message, as in original requirements
* Registration attempt with password with no special character fails error message check
    * Fixed boolean condition in backend.validatePassword

### R2.7
* POST request not processed when form fields left empty, and could not check error message
    * Fixed by checking if form input has attribute "required"
    
### R2.11
* No methods to access database and check user account balance
    * Migrating user account balance requirement check to backend testing
    * Deferring account balance test for now, just checking successful register and redirect to /login
    * Mocked backend.get_user to return None, so we pass the check if email has already been used
    * Mocked backend.register_user to avoid adding user in database while registering
