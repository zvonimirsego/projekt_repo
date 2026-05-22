import pytest
from database.py_classes import Loan
from datetime import date


@pytest.fixture
def loan():
    loan = Loan(
        "1111",
        "user@gmail.com",
        "EQ001",
        date.today(),
        date.today(),
        False
    )
    return loan

def test_loan_init(loan):

    assert loan.id_user == "user@gmail.com"

def test_loan_default_returned(loan):

    assert loan.returned is False