SeetGeek Web App Design Document
---------------------------
| File | Class/Method | Description |
|--|--|--|
| Models | class User | A user model which defines the sql table, with identification, login, name and account balance information|
|Frontend | login_get()| Renders the login page. |
| | login_post() | Gets login information from form request. Calls backend to validate login info, and if valid logs a user then redirects to user home page. |
| | logout() | Logs out user and redirects to home page. |
| | register_get() | Renders register page, or redirects to user home page if already logged in. |
| | register_post() | Gets registration information from form request. Calls backend to validate registration info, and if valid, registers user in the backend and database, then redirects to login page.
| | authenticate(inner_function) | Decoration function, which calls backend to verify if user is logged in before running inner_function, otherwise redirects to login page.
| | profile(user) | |
| Backend | validateEmail(email) | Uses the email_validator package to ascertain supplied email string as valid email adress, returns True or False. |
| | validatePassword(password) | Checks supplied password string against conditions for password strength, returns True or False. |
| | validateUserName(username) | Checks supplied username string against conditions for username validity, returns True or False. |
| | get_user(email) | Queries database for User object matching the supplied email adress, then returns it |
| | login_user(email, password) | Calls get_user(email) and check_password_hash from security package to validate email and password combination for the given User, returns User if valid and nothing otherwise.
| | register_user(email, name, password, password2) | Hashes supplied password, creates new User object from parameters with an account balance of 5000, and commits User to database.|
| | get_all_tickets() | |


