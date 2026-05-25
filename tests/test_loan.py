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
        id_loan="1111",
    )
    return loan


# unit test
def test_loan_init(loan):

    assert loan.id_user == "user@gmail.com"


# unit test
def test_loan_default_returned(loan):

    assert loan.returned is False


# unit test
def test_loan_returned_true():

    loan = Loan(1, "u", "eq", date.today(), date.today(), True)

    assert loan.returned is True


def test_loan_fetch_fail():
    loan = Loan.fetch(99999)

    assert loan is None
