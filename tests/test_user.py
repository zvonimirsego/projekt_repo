import pytest
from datetime import date, timedelta
from classes import Users, Equipment, Admin
from db_tables import  db_engine, Loan as DBLoan, Equipment as DBEquipment, Users as DBUser
from sqlmodel import  Session, select 
from sqlalchemy import text

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
            condition="good",
            available=True
        )

        session.add(eq)
        session.commit()

    yield eq

    with Session(db_engine) as session:

        equipment = session.exec(
            select(DBEquipment).where(
                DBEquipment.id_equipment == "AA001"
            )
        ).first()

        if equipment:
            session.delete(equipment)
            session.commit()


@pytest.fixture
def test_user():

    user = Users(
        "levine@gmail.com",
        "Ken",
        "Levine",
        "1234"
    )

    user.add()

    yield user

    with Session(db_engine) as session:

        db_user = session.exec(
            select(DBUser).where(
                DBUser.id_email == "levine@gmail.com"
            )
        ).first()

        if db_user:
            session.delete(db_user)
            session.commit()

class TestReservation:
    def test_make_reservation_success(self, equipment):
        user = Users(
            "levine@gmail.com",
            "Ken",
            "Levine",
            "1234"
        )
        
        reservation = user.makeReservation("AA001", date.today(), date.today() + timedelta(days=10))

        assert reservation is True

        with Session(db_engine) as session:
            statement = select(DBLoan).where(
                DBLoan.id_user == "levine@gmail.com",
                DBLoan.id_equipment == "AA001"
                )
            reservation_db = session.exec(statement).first()
            assert reservation_db is not None
            
    def test_makeResrvation_fail_on_borrowed_equipment(self, equipment):
        user = Users(
            "ace@gmail.com",
            "Elizabeth",
            "Devit",
            "4321"
        )
        user.makeReservation(
            "AA001",
            date.today(),
            date.today() + timedelta(days=14)
        )
        with Session(db_engine) as session:

            statement = select(DBEquipment).where(
            DBEquipment.id_equipment == "AA001"
            )
            equipment = session.exec(statement).first()
            equipment.available = False

            session.commit()


        with pytest.raises(ValueError, match="Equipment is allready borrowed"):
            user.makeReservation(
            "AA001",
            date.today(),
            date.today() + timedelta(days=14)
        )
             
        
    def test_makeReservation_fail_on_wrong_date(self, equipment):
        user = Users(
            "levine@gmail.com",
            "Ken",
            "Levine",
            "1234"
        )
        with pytest.raises(ValueError, match="Wrong date"):
            user.makeReservation(
                "AA001",
                date.today(),
                date.today() - timedelta(days=2)
            )

    def test_makeReservation_fail_on_non_existing_equipment(self, equipment):
        user = Users(
            "levine@gmail.com",
            "Ken",
            "Levine",
            "1234"
        )
        with pytest.raises(ValueError, match="Equipment doesn't exists"):
            user.makeReservation(
                "ZZ999",
                date.today(),
                date.today() + timedelta(days=2)
            )
        
    def test_delete_reservation(self, equipment):
        user = Users(
            "ace@gmail.com",
            "Elizabeth",
            "Devit",
            "4321"
        )
        user.makeReservation(
                "AA001",
                date.today(),
                date.today() + timedelta(days=2)
            )
        
        with Session(db_engine) as session:
            statement = select(DBLoan).where(
                DBLoan.id_user == "ace@gmail.com"
                )
            loan = session.exec(statement).first()
            assert loan is not None
        result = user.deleteReservation(loan.id_loan)
        assert result is True

        with Session(db_engine) as session:
            statement = select(DBLoan).where(
                DBLoan.id_loan == loan.id_loan
            )
        deleted_loan = session.exec(statement).first()

        assert deleted_loan is None

def test_add_success(test_user):

    with Session(db_engine) as session:

        db_user = session.exec(
            select(DBUser).where(
                DBUser.id_email == "levine@gmail.com"
            )
        ).first()

        assert db_user is not None

def test_add_duplicate_user():
    user = Users(
        "duplicate@gmail.com",
        "Ken",
        "Levine",
        "1234"
        )
    user.add()

    with pytest.raises(ValueError, match="User with this email allready exists"):
        user.add()

def test_fetch():
    u = Users("fetch@gmail.com","Elizabeth","Devit","4321")
    u.add()
    user = Users.fetch("fetch@gmail.com")

    assert user is not None
    assert user.email == "fetch@gmail.com"

def test_fetch_fail():
    user = Users.fetch("nepostoji@gmail.com")
    assert user is None