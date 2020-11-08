<<<<<<< HEAD

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
| | errorhandler(404), notfound(e) | For any requests outside of specifications, render 404 page not found page, with option to redirect back to home page. | 
| Backend | validateEmail(email) | Uses the email_validator package to ascertain supplied email string as valid email adress, returns True or False. |  
| | validatePassword(password) | Checks supplied password string against conditions for password strength, returns True or False. |  
| | validateUserName(username) | Checks supplied username string against conditions for username validity, returns True or False. |  
| | get_user(email) | Queries database for User object matching the supplied email adress, then returns it |  
| | login_user(email, password) | Calls get_user(email) and check_password_hash from security package to validate email and password combination for the given User, returns User if valid and nothing otherwise.  
| | register_user(email, name, password, password2) | Hashes supplied password, creates new User object from parameters with an account balance of 5000, and commits User to database.|  
| | get_all_tickets() | |
=======
SeetGeek Web App Design Document
---------------------------
| File | Class/Method | Description |
|--|--|--|
| Models | class User | A user model which defines the sql table, with identification, login, name and account balance information|
| | class Tickets | A ticket model which defines the sql table, with identification, seller email, name, date, quantity and price |
|Frontend | login_get()| Renders the login page. |
| | login_post() | Gets login information from form request. Calls backend to validate login info, and if valid logs a user then redirects to user home page. |
| | logout() | Logs out user and redirects to home page. |
| | register_get() | Renders register page, or redirects to user home page if already logged in. |
| | register_post() | Gets registration information from form request. Calls backend to validate registration info, and if valid, registers user in the backend and database, then redirects to login page.
| | authenticate(inner_function) | Decoration function, which calls backend to verify if user is logged in before running inner_function, otherwise redirects to login page.
| | profile(user) | Gets all tickets. Then filters through tickets and remove expired tickets. Returns render template and calls index.html with users and tickets information |
| | sell_form_post() | Gets sell information from form request. Calls backened and adds ticket to tickets database and redirects user to sell page |
| | buy_form_post() | Gets buy information from form request. Calls backened to make ticket unavailable and redirects user to buy page |
| | update_form_post() | Gets update information from form request. Calls backened to update ticket and redirects user to update page |
| Backend | validateEmail(email) | Uses the email_validator package to ascertain supplied email string as valid email adress, returns True or False. |
| | validatePassword(password) | Checks supplied password string against conditions for password strength, returns True or False. |
| | validateUserName(username) | Checks supplied username string against conditions for username validity, returns True or False. |
| | get_user(email) | Queries database for User object matching the supplied email adress, then returns it |
| | login_user(email, password) | Calls get_user(email) and check_password_hash from security package to validate email and password combination for the given User, returns User if valid and nothing otherwise.
| | register_user(email, name, password, password2) | Hashes supplied password, creates new User object from parameters with an account balance of 5000, and commits User to database.|
| | get_all_tickets() | Gets all tickets in tickets database and returns a list of all tickets|
| | sell_ticket(name,quantity,price,expireDate) | Adds ticket with input parameters and commits new addition to tickets database |
| | update_ticket(name,quantity,price,expireDate) | Updates ticket with parameters and commits new changes to tickets database|
| | buy_ticket(name,quantity) | Deletes the ticket from the tickets database|
>>>>>>> 9f6d1a5030ba4dacc41948b8fd24ac62765a077d
