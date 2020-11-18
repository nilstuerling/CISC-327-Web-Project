R7 Frontend Failure Report
==========================

R7.1
----
* Opening endpoints for ticket transactions (`/buy`, `/sell`, `/update`) in the browser (this would be GET request) resulted in an internal error and a response to the user saying the method is not available
	* Fixed by adding the proper methods to implement GET requests to said endpoints. It redirects to `/`. Doing so will either send them to the profile page where they can properly manage tickets (if they are logged in), or redirect them again to the /login page so they can login or register (if they are not logged in).
* Making POST requests to endpoints for ticket transactions (`/buy`, `/sell`, `/update`) while not logged in resulted in an error
	* Fixed by adding a check to make sure the user was logged in. If they are not, it redirects them to `/`, which then redirects to the login page where they can login or register
