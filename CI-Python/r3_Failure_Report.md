### Assignment 3 - R3 Failure Report:

**R3 All** - Error in testing caused by unpatched server and backend. Fixed by patching up the backend and returning a fixed response to test the frontend part of the application.

**R3.5** - Fixed the expired sort feature within the frontend file. Now it works with a list of dictionaries, and filters out all the expired tickets. 

**R3.6** - Fixed the sell feature in the frontend file. Now message is displayed when a ticket is successfully added to the ticket database else displays error message. 

**R3.7** - Fixed the buy feature in the frontend file. Now message is displayed when a ticket is sold successfully else prints error message. 

**R3.8** - Fixed the update feature in the frontend file. Now message is displayed when a ticket is successfully updated else prints error message.

**R3.9 & R3.10 & R3.11 ** - Test case was unable to differentiate between the different forms on the / page. The frontend functions sell_form_post, buy_form_post, and update_form_post take their dedicated forms information as they call the form specific identifiers. Thus the method should work, however failed to show this in testing. 

