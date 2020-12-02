Backend Design Document  
--------  
The following table lists and documents all functions in the file backend.py

| Purpose | Function | Description |  
| ------------ | ----------- |  ---- |
| Ticket Validation | validateTicketName(ticketName) | Takes a string input as ticket name and returns True if meeting formatting requirements, False otherwise |
| | validateTicketExists(ticketName) | takes a string input as ticket name, queries database for ticket corresponding with name, and returns True if ticket is in database, False otherwise |
|  | validateTicketQuantity(ticketQuantity) | takes an integer input as ticket quantity and returns True if within valid range (as defined in requirements), False otherwise |
| Ticket Transaction Validation | validateEnoughTickets(buyQuantity, ticketName) | takes as string input ticket name and integer input the desired quantity to buy. Queries database for available quantity of that ticket, and returns False if buyQuantity exceeds available amount, True otherwise |
| | validateBalanceEnough(buyQuantity, ticketName, user) | takes as string input ticket name, integer input buying quantity, and a user instance. Queries database for ticket information, computes price of buying quantity of tickets with tax, and returns True if User has a sufficient account balance to pay, False otherwise
| | validateTicketPrice(ticketPrice) | takes an integer input as ticket price and returns True if within valid range (as defined in requirements), False otherwise |
| | validateTicketExpiryDate(date) | takes a string input as  ticket date, and attempts to parse it as a valid date. Returns True if parsed successfully as a date later than current date, False otherwise |
| Ticket Transaction | get_all_tickets() | Queries database and returns all stored tickets |
| | sell_ticket(userEmail, name, quantity, price, expireDate) | Creates new ticket with fields from supplied argument and stores it in database | 
| | update_ticket(userEmail, name, quantity, price, expireDate) | Updates ticket with parameters and commits new changes to tickets database |
| | buy_ticket(userEmail, name, quantity) | Adds specified ticket to user account, removing specified quantity from database | 
| Misc | format_date(ticketDate) | Formats date from string input into printable string |
| User Database | get_user(email) | Function that returns User object from database from unique email address |
| | login_user(email, password) | Logs user in session if valid email/password pair | 
| | register_user(email, name, password) | Registers and adds user to database with valid supplied parameters