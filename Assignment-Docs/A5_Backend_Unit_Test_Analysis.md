
# Backend Unit Test Analysis
### Ticket selling, buying and updating (R4, R5, R6)


The backend method unit tested is comprised of all ticket field validations, that is the methods:
* validateTicketName
* validateTicketQuantity
* validateTicketPrice
* validateTicketExpiryDate

The unit test cases were created using a mixture of the white box condition and path coverage methods. 

This systematic approach may be executed as follows: for a given function, we perform regular path coverage analysis, and find independent paths that cover all scopes. Then, for every independent path, we perform condition coverage analysis of that path. This is a clear and informed testing procedure, and by its simple nature of staggering two known systematic testing methods, we have a measure of completeness. Thus, this mixed approach is itself also systematic.


This allows us to cover every combination of boolean condition, up to the point of returning from the function. For example, for the function validateTicketName, if the input chosen leads to entering the first if statement block, we immediately return False from the function, and it is pointless to consider any latter boolean condition for that input partition. In this way, we get the benefits of having testing efficiency as in path coverage (saving on action minutes), as well as having the most thorough input partitioning, where we may test boundary cases (which is very important especially in user applications such as this one).


#### Test Cases:

| Backend Function | Input Partition | Input | Expected Output |
| --- | --- | --- | --- |
| validateTicketName | not len(ticketName) > 60, not ticketName[0] == ' ', not ticketName[-1] == ' ', alphanumeric | "ticket1" | True |
| | not len(ticketName) > 60, ticketName[0] == ' ' | " ticket" | False |
| | not len(ticketName) > 60, ticketName[-1] == ' ' | "ticket " | False |
| | not len(ticketName) > 60, not ticketName[0] == ' ', not ticketName[-1] == ' ', not alphanumeric | "!!!" | False |
| | len(ticketName) > 60 | string of length 61 | False |
| validateTicketQuantity | Lower boundary | 0 | True |
| | Upper boundary | 100 | True |
| | ticketQuantity < 0 | -1 | False |
| | ticketQuantity > 100 | 101 | False |
| validateTicketPrice | Lower boundary | 10 | True |
| | Upper boundary | 100 | True |
| | ticketPrice < 10 | 9 | False |
| | ticketPrice > 100 | 101 | False |
| validateTicketExpiryDate | ticketDate > today | tomorrow | True |
|  | Boundary date | today | True |
| | not len(date) == 8 | "" | False |
| | ticketDate < today | yesterday | False |
| | Value Error in converting string to date | "20201332" | False |



Implementing and running the test cases as above, we get the expected outputs for all cases except the following:

* FAILURE in testing boundary date in function validateTicketExpiryDate. Returns False when it should return True.
	* Caused by extraneous hour, minute and seconds comparison
	* Fixed by changing datetime instances to date instances
	* Removed extraneous comparison ticketDate != today (already covered in ticketDate < today)

