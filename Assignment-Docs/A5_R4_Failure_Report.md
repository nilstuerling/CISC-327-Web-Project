## Assignment 5 - Failure Report:

### R4 Frontend Failure Report

**R4.5** - Tested validation for ticket expiry date format with string "2020 12 10". This test passed although there are spaces within the date (thereby making it an invalid date format). After further investigation, this is because the date field for the sell form **does not allow for spaces** (spaces are automatically removed as the field type is "number"). As a result, the input "2020 12 10" is actually truncated to "20201210" when entered into the form. This test case was removed from testing (as it is no longer a possible case), no code changes were made.

**R4.6** - Added functionality with sell_ticket backend function to support the ability to propogate error messages to the profile page when business logic fails. Although this backend functionality is mocked during frontend testing, the function still needed modification to reflect the same return type and values the mock would be providing.

**Additional** - Modified the ticket expiry date validation to allow for tickets to be sold with an expiry date on the *same day* (thereby also allowing tickets to be purchased on the current day). This change was also reflected for the frontend profile page to allow display of tickets with the current date.