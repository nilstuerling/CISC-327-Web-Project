# Integration Testing Analysis and Failure Report


In integrating the buy, sell and update features into the current build, some considerations to the current project template were made.
Specifically, previous modifications which were made to drop all data from the database each time the server was started, were reverted.
We then get that database entries persist between test cases using the regular "server" pytest fixture. A new pytest fixture was
created (in Web-App/qa327_test/conftest.py), called "fresh_server", where, when used, database entries are dropped between test cases.
This fixture was used for the integration testing.

Integration testing was implemented in three test cases, the first of which follows the path of a user registering, logging in,
and posting a ticket for sale. In the second test case, as a setup we recreate the selling path from the first test case (wihtout
any of the assertions), then, logged in as the same user, we attempt to update ticket information for the ticket we just sold.
In the last test case, we once again set up the test case with the ticket selling path, then follow the path of a second user registering,
logging in, and buying the tickets listed from the first user.

In implementing and running these test cases, multiple failures were encountered which lead to some drastic changes in the buy, sell and
update backend functions, which were previously simply mocked in testing and were not implemented properly. Failures and their appropriate
fixes are documented below.

### Failure Report


#### Ticket Selling
* Failure in selling path, SQLAlchemy IntegrityError
    * We had persistent ticket data from a previous testing, and we can't sell two tickets from same account
        * Fixed by decorating integration test with "fresh_server" fixture
        * Fixed by removing UNIQUE constraint to Tickets "email" field in database (in models.py)
        * Added proper error handling in frontend /sell POST for selling tickets of name already listed

#### Ticket Updating
* Ambiguous specifications while implementing test case; what exactly are we updating?
    * Going forward, assuming we specify a ticket name to update (from your own listings)
    * Other fields (quantity, price, expiry date) are the values to change
    * Updated field labels in index.html to make this functionality more obvious
* Previous fix of making ticket email non-unique breaks current implementation
    * Fixed by adding UNIQUE constraint to (email, name) pair in Tickets table, in models.py
    * Re-implemented backend function to properly query for, and update the specified ticket
    * Added extra error handling in frontend /update POST
    * Added proper error handling in frontend /sell POST for selling tickets of name already listed
        * Retroactive /sell path fix needed, since new (email, name) UNIQUE constraint can throw more IntegrityError's


#### Ticket buying
* Failure in ticket buying: backend function is not implemented
    * Implemented backend.buy_ticket
    * Migrated calls to validateEnoughTickets and validateBalanceEnough from frontend to backend
    * Fixed with proper querying of database by ticket name
        * Iterates through through results, sorted by price
        * Buys from first result with sufficient quantity (which will be cheapest option)
    * Returns error message, if any, to frontend
* Failure in user balance deduction: invalid operation between database Numeric type and python float
    * Fixed by converting total ticket price to Decimal before deduction, in backend.buy_ticket
    * Also applied conversion to test case implementation accordingly

#### Previous testing failure
* From having changed a few backend function return styling (returning error message string instead of True/False)
    * Updated backend patching accordingly
* From having changed html template (exact wording of headings/text)
   * Updated appropriate assertions in test cases accordingly