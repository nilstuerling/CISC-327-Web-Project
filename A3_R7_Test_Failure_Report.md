R7 Frontend Failure Report
==========================

R7.1
----
* Opening endpoints for ticket transactions (`/buy`, `/sell`, `/update`) in the browser (this would be GET request) resulted in an internal error and a response to the user saying the method is not available
	* Fixed by adding the proper methods to implement GET requests to said endpoints. It redirects to `/` if they are logged in, thus taking them to their userpage where they can properly interact with buying, selling, and updating tickets. If they are not logged in, it redirects to `/login`, where they can either login or register.

* Making POST requests to endpoints for ticket transactions (`/buy`, `/sell`, `/update`) while not logged in resulted in an error
	* Fixed by adding a check to make sure the user was logged in. If they are not, it redirects them to `/login`, where they can login or register. If they are, it continues with the rest of the action as normal.
