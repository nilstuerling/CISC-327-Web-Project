### Assignment 3 - Backend Unit Test Analysis

Unit tests were created for backend methods: _validateEmail_ and _validatePassword_.

Inputs for _validateEmail_ can be partitioned into two types, valid and invalid emails. Emails are valid/invalid depending on if they followthe addr-spec defined in RFC 5322. Consequently, there were two test cases, one for valid email input and one for an invalid email input, testing that _validateEmail_ returned _True_ and _False_ for the inputs, respectively.

Inputs for _validatePassword_ can again by partitioned into two types, valid and invalid passwords. However, passwords fail validity on more conditions than emails (too short, no uppercase characters, no lowercase characters, no special characters) and therefore require more test cases. As a result, there were five test cases, one for testing each failure condition listed earlier, and a final test case checking a valid password, returning _False, False, False, False,_ and _True_ for the inputs, respectively.