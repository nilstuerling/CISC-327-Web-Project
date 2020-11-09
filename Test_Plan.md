Test Plan
=========

### How test cases of different levels (frontend, backend units, integration) are organized
* Within the qa327\_test directory, there are folders for frontend, backend, and integration tests. Each folder will contain python files for each unit test to be run. For example, qa327\_test/frontend/homepage.py will contain a test to confirm that if a user is logged in, the #welcome\_header is shown, and qa327\_test/backend/register.py will contain a test to confirm that provided inputs for email, name, and password match the required values


### The order of the test cases (which level first which level second).
* Backend test cases will be run first as the backend is the area where any incorrectly verified inputs are actually processed. Frontend testing will be done second to confirm that the user receives the appropriate feedback based on their inputs. Lastly, integration testing will be done to make sure that each unit test, as well as the frontend and the backend, work together after having verified that they work on their own individually.

### Techniques and tools used for testing.
* All testing will be done with the Pytest library, which will run tests for Frontend, Backend, and Integration testing.
* Frontend and Integration tests will be done using the Selenium API. It will allow us to replicate user interactions with the browser and then test if the output from those interactions are as intended. 
* Tests will be broken up into Unit Tests. Different actions of the backend, such as creating user accounts, logging in and out, and buying/selling tickets will each be divided into units and tested separately. Methods like input partitioning and shotgun hybrid testing will be used to verify that each unit creates the correct outputs.

### Environments (all the local environment and the cloud environment) for the testing.
* A local test environment is done using Python and the Flask library.

### Responsibility (who is responsible for which test case, and in case of failure, who should you contact)
* Each person will be responsible for the test cases corresponding to the requirements they detailed in Assignment 1. Additionally, using git, we can see who made modifications to both source code and test cases. Using this, when a test fails, we can both contact the manager for that certain test, as well as whoever made the last edit to the code base that caused the test to fail when it previously passed. 

### Budget Management (you have limited CI action minutes, how to monitor, keep track and minimize unnecessary cost)
* In order to use the Github Action minutes most efficiently, all changes to the codebase will go through pull requests that must be approved by all members. This allows for the best chance of catching any mistakes before the tests run again, thus minimizing the number of tests that will be run. Furthermore, Github has an option to provide a usage report on Actions. By reviewing the usage report after Action tests are run, we can determine whether we are approaching the usage cap and adjust our testing frequencies accordingly.
