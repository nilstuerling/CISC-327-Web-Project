Assignment 5 - Failure Report:
==============================

R6 Frontend Failure Report
--------------------------

### ALL
* Due to a change the in codebase, the format of ticket dates stored on the server changed. To adjust for this in R6 tests, the mocked tickets needed to have their date changed from `20201224` to `24/12/2020`.

* The frontend validation of ticket buying would check against certain validations, then try to buy the ticket and validate more when trying to buy. This was changed so that if any validations failed, it would immediately return an error to the user before trying to buy.

### R6.4
* The `@patch` for the test to mock tickets in database only altered the `get_all_tickets()` function. However, our backend validation queried the tickets directly, meaning the `@patch` didn't actually mock any tickets for the test to check against. By changing `validateTicketExists` and `validateEnoughTickets`, to use the `get_all_tickets()` function, the tests can now properly mock tickets for sale, and then validate the features of the `/buy` endpoint

### R6.5
* The same as with regards to R6.4; however, the change was made to the function `validateBalanceEnough`
