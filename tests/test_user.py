import pytest
from database.py_classes import Users
from database.db_tables import (
    db_engine,
    Loan as DBLoan,
    Equipment as DBEquipment,
    Users as DBUser,
)
from sqlmodel import Session, select
from sqlalchemy import text
from datetime import date, timedelta


@pytest.fixture(autouse=True)
def clean_db():

    yield

    with Session(db_engine) as session:

        session.exec(text("DELETE FROM loan"))
        session.exec(text("DELETE FROM equipment"))
        session.exec(text("DELETE FROM users"))

        session.commit()


@pytest.fixture
def equipment():

    with Session(db_engine) as session:

        eq = DBEquipment(
            id_equipment="AA001",
            equipment_name="Laptop",
            condition="used",
            available=True,
        )

        session.add(eq)
        session.commit()

    yield eq

    with Session(db_engine) as session:

        equipment = session.exec(
            select(DBEquipment).where(DBEquipment.id_equipment == "AA001")
        ).first()

        if equipment:
            session.delete(equipment)
            session.commit()


@pytest.fixture
def test_user():

    user = Users("user@gmail.com", "Ken", "Levine", "1234")

    user.add()

    yield user

    with Session(db_engine) as session:

        db_user = session.exec(
            select(DBUser).where(DBUser.id_email == "user@gmail.com")
        ).first()

        if db_user:
            session.delete(db_user)
            session.commit()


def test_user_init(test_user):

    user = test_user

    assert user.email == "user@gmail.com"
    assert user.first_name == "Ken"
    assert user.is_admin is False


def test_user_default_admin(test_user):

    assert test_user.is_admin is False


class TestReservation:
    def test_make_reservation_success(self, equipment, test_user):
        reservation = test_user.makeReservation(
            "AA001", date.today(), date.today() + timedelta(days=14)
        )

        assert reservation is True

        with Session(db_engine) as session:
            statement = select(DBLoan).where(
                DBLoan.id_user == "user@gmail.com", DBLoan.id_equipment == "AA001"
            )
            reservation_db = session.exec(statement).first()
            assert reservation_db is not None

    def test_makeResrvation_fail_on_borrowed_equipment(self, equipment, test_user):
        user = test_user
        user.makeReservation("AA001", date.today(), date.today() + timedelta(days=14))
        with Session(db_engine) as session:

            session.commit()

        with pytest.raises(ValueError, match="Oprema nije dostupna"):
            user.makeReservation(
                "AA001", date.today(), date.today() + timedelta(days=14)
            )

    def test_makeReservation_fail_on_non_existing_equipment(self, test_user):
        user = test_user
        with pytest.raises(ValueError, match="Oprema ne postoji"):
            user.makeReservation(
                "ZZ999", date.today(), date.today() + timedelta(days=14)
            )

    def test_delete_reservation(self, equipment, test_user):
        user = test_user
        user.makeReservation("AA001", date.today(), date.today() + timedelta(days=14))

        with Session(db_engine) as session:
            statement = select(DBLoan).where(DBLoan.id_user == user.email)
            loan = session.exec(statement).first()
            assert loan is not None
        result = user.deleteReservation(loan.id_loan)
        assert result is True

        with Session(db_engine) as session:
            statement = select(DBLoan).where(DBLoan.id_loan == loan.id_loan)
            deleted_loan = session.exec(statement).first()

        assert deleted_loan is None


def test_add_success(test_user):

    with Session(db_engine) as session:

        db_user = session.exec(
            select(DBUser).where(DBUser.id_email == "user@gmail.com")
        ).first()

        assert db_user is not None


def test_add_duplicate_user(test_user):
    with pytest.raises(ValueError, match="Korisnik sa ovim email-om već postoji"):
        test_user.add()


def test_fetch():
    u = Users("fetch@gmail.com", "Elizabeth", "Devit", "4321")
    u.add()
    user = Users.fetch("fetch@gmail.com")

    assert user is not None
    assert user.email == "fetch@gmail.com"


def test_fetch_fail():
    user = Users.fetch("nepostoji@gmail.com")
    assert user is None
