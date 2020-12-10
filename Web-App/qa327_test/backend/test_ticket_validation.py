#######################
# Backend Unit Testing
# Ticket selling, buying and updating (R4, R5, R6)
# Testing the ticket validation functions
# Refer to Assignment-Docs/A5_Backend_Unit_Test_Analysis.md for complete documentation
####################

import pytest
from datetime import datetime, timedelta
from qa327.backend import validateTicketName, validateTicketQuantity
from qa327.backend import validateTicketPrice, validateTicketExpiryDate


###################
# validateTicketName test cases

# Input partitioning
validName = "ticket1"
leadingSpaceName = " ticket"
trailingSpaceName = "ticket "
nonAlphaName = "!!!"
longName = ""
for i in range(0, 61): longName += "a"


class TestTicketName:
    def test_valid_name(self):
        assert validateTicketName(validName)

    def test_space_name(self):
        assert not validateTicketName(leadingSpaceName)
        assert not validateTicketName(trailingSpaceName)

    def test_alpha_name(self):
        assert not validateTicketName(nonAlphaName)

    def test_long_name(self):
        assert not validateTicketName(longName)


###################
# validateTicketQuantity test cases

# Input partitioning
validQuant1 = 1
validQuant2 = 100
lowQuant = -1
highQuant = 101


class TestTicketQuantity:
    def test_boundary_quant(self):
        assert validateTicketQuantity(validQuant1)
        assert validateTicketQuantity(validQuant2)

    def test_low_quant(self):
        assert not validateTicketQuantity(lowQuant)

    def test_high_quant(self):
        assert not validateTicketQuantity(highQuant)


###################
# validateTicketPrice test cases

# Input partitioning
validPrice1 = 10
validPrice2 = 100
lowPrice = 9
highPrice = 101


class TestTicketPrice:
    def test_bound_price(self):
        assert validateTicketPrice(validPrice1)
        assert validateTicketPrice(validPrice2)

    def test_low_price(self):
        assert not validateTicketPrice(lowPrice)

    def test_high_price(self):
        assert not validateTicketPrice(highPrice)


###################
# validateTicketExpiryDate test cases

# Input partitioning
dateFormat = "{year:n}{month:02d}{day:02d}"
shortDate = ""
todayDatetime = datetime.today()
today = dateFormat.format(year=todayDatetime.year, month=todayDatetime.month, day=todayDatetime.day)
yesterdayDatetime = todayDatetime - timedelta(1)
yesterday = dateFormat.format(year=yesterdayDatetime.year, month=yesterdayDatetime.month, day=yesterdayDatetime.day)
tomorrowDatetime = todayDatetime + timedelta(1)
tomorrow = dateFormat.format(year=tomorrowDatetime.year, month=tomorrowDatetime.month, day=tomorrowDatetime.day)
invalidDate = "20201332"


class TestTicketDate:
    def test_valid_date(self):
        assert validateTicketExpiryDate(tomorrow)

    def test_short_date(self):
        assert not validateTicketExpiryDate(shortDate)

    def test_bound_date(self):
        assert validateTicketExpiryDate(today)

    def test_yesterday_date(self):
        assert not validateTicketExpiryDate(yesterday)

    def test_invalid_date(self):
        assert not validateTicketExpiryDate(invalidDate)




