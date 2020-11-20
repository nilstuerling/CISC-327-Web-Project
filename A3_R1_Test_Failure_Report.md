### Assignment 3 - R1 Failure Report:

**R1.3** - Fixed implementation in frontend logic for GET request to /login to redirect to user profile page if "logged_in" was in the current session

**R1.6** - Test case different from its respective test spec in R1 requirements document. Checking for non-empty inputs is done by ensuring that the form elements _#email_ and _#password_ have the _required_ attribute, thereby ensuring that input cannot be empty.

**R1.8** - Fixed implementation for password validation in logic due to test case. Test case did not fail on case where password was missing a special character. Backend logic fixed to return an invalid password response on this condition (previous logic was not checking for special characters properly).

**R1.9** – To clarify, the error message response for this requirement was used in all previous formatting errors. Each of the previous formatting errors checks for this error message response.

**R1.11** – Test case different from its respective test spec in R1 requirements document. No need to enter invalid user&#39;s credentials, instead the test just mocks an invalid return from the database.