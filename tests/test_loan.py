import pytest
from database.py_classes import Loan
from datetime import date


@pytest.fixture
def loan():
    loan = Loan(
        id_user="user@gmail.com",
        id_equipment="EQ001",
        starting_date=date.today(),
        due_date=date.today(),
        returned=False,
        id_loan="1111"
    )
    return loan

def test_loan_init(loan):

    assert loan.id_user == "user@gmail.com"

def test_loan_default_returned(loan):

    assert loan.returned is False