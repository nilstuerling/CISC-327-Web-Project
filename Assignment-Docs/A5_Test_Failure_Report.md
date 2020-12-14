Assignment 5 - Failure Report:  
==============================  
### Template Changes

Reverted previous change of adding *db.drop_all()* on app startup. We had previously implemented this change to have safer live testing. As an alternative solution, configured a new server thread and pytest fixture, with *db.drop_all()* so we may have our safe testing when needed but still have persistent data between actual uses of the application.
<br>
### R4 Frontend Failure Report 
  
**R4.5** 
* Tested validation for ticket expiry date format with string "2020 12 10". This test passed although there are spaces within the date (thereby making it an invalid date format). After further investigation, this is because the date field for the sell form **does not allow for spaces** (spaces are automatically removed as the field type is "number"). As a result, the input "2020 12 10" is actually truncated to "20201210" when entered into the form. This test case was removed from testing (as it is no longer a possible case), no code changes were made.  
  
**R4.6** 
* Added functionality with sell_ticket backend function to support the ability to propogate error messages to the profile page when business logic fails. Although this backend functionality is mocked during frontend testing, the function still needed modification to reflect the same return type and values the mock would be providing.  
  
**Additional** 
* Modified the ticket expiry date validation to allow for tickets to be sold with an expiry date on the *same day* (thereby also allowing tickets to be purchased on the current day). This change was also reflected for the frontend profile page to allow display of tickets with the current date.

<br>

### R5 Frontend Failure Report  
  
**R5 All** 
* Error due to invalid date format. Fixed by changing the date format of the update date input from the input format of YYYYMMDD to DD/MM/YYYY.  
  
**R5.7** 
* Conducted some changes to frontend update_form_post and backend update_ticket. So that if the business logic fails then the error message "Unable to update ticket" will be displayed.


  <br>
### R6 Frontend Failure Report 
  
**R6 All**  
* Due to a change the in codebase, the format of ticket dates stored on the server changed. To adjust for this in R6 tests, the mocked tickets needed to have their date changed from `20201224` to `24/12/2020`.  
  
* The frontend validation of ticket buying would check against certain validations, then try to buy the ticket and validate more when trying to buy. This was changed so that if any validations failed, it would immediately return an error to the user before trying to buy.  
  
**R6.4**  
* The `@patch` for the test to mock tickets in database only altered the `get_all_tickets()` function. However, our backend validation queried the tickets directly, meaning the `@patch` didn't actually mock any tickets for the test to check against. By changing `validateTicketExists` and `validateEnoughTickets`, to use the `get_all_tickets()` function, the tests can now properly mock tickets for sale, and then validate the features of the `/buy` endpoint  

**R6.5**  
* The same as with regards to R6.4; however, the change was made to the function `validateBalanceEnough`