Assignment 5 - Failure Report:
==============================

R6 Frontend Failure Report
--------------------------

### R6.4 & R6.5
The `@patch` for the test to mock tickets in database only altered the `get_all_tickets()` function. However, our backend validation queried the tickets directly, meaning the `@patch` didn't actually mock any tickets for the test to check against. By changing `validateTicketExists` and `validateEnoughTickets`, to use the `get_all_tickets()` function, the tests can now properly mock tickets for sale, and then validate the features of the `/buy` endpoint
