from database.db_tables import (
    db_engine,
    Users as DBUsers,
    Loan as DBLoan,
    Equipment as DBEquipment,
)
from sqlmodel import Session, select


class Loan:
    def __init__(
        self, id_loan, id_user, id_equipment, starting_date, due_date, returned
    ):
        self.id_loan = id_loan
        self.id_user = id_user
        self.id_equipment = id_equipment
        self.starting_date = starting_date
        self.due_date = due_date
        self.returned = returned


class Users:
    def __init__(self, email, first_name, last_name, password, is_admin=False):
        # za is_admin vidjeti file na desktopu
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    # Morao sam dodati malu izmjenu kako bi se dostupnost opreme promjenila nakon posudbe, uz provjeru ako je dostupna
    def makeReservation(self, id_equipment, starting_date, due_date):
        with Session(db_engine) as session:
            # provjeri dostupnost
            equipment = session.exec(
                select(DBEquipment).where(DBEquipment.id_equipment == id_equipment)
            ).first()
        if not equipment:
            raise ValueError("Oprema ne postoji")
        if not equipment.available:
            raise ValueError("Oprema nije dostupna")

        statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan.desc())
        last_id = session.exec(statement).first()
        next_id = 1 if last_id is None else last_id + 1

        db_loan = DBLoan(
            id_loan=next_id,
            id_user=self.email,
            id_equipment=id_equipment,
            start_date=starting_date,
            due_date=due_date,
            returned=False,
        )
        session.add(db_loan)

        # postavi available na False
        equipment.available = False
        session.add(equipment)

        session.commit()
        return True

    def deleteReservation(self, id_loan):
        with Session(db_engine) as session:
            statement = select(DBLoan).where(
                DBLoan.id_loan == id_loan, DBLoan.id_user == self.email
            )
            loan = session.exec(statement).first()
            if loan:
                session.delete(loan)
                session.commit()
                return True
            return False

    # dodati naredbu za fetch i za addanje u bazu

    def add(self):
        with Session(db_engine) as session:
            existing = session.exec(
                select(DBUsers).where(DBUsers.id_email == self.email)
            ).first()

            if existing:
                raise ValueError("Korisnik sa ovim email-om već postoji")

            db_user = DBUsers(
                id_email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_admin=self.is_admin,
            )
            try:
                session.add(db_user)
                session.commit()
            except Exception as e:
                if "UNIQUE constraint failed: users.id_email" in str(e):
                    raise ValueError("Korisnik sa ovim email-om već postoji")
                raise

    # Briše usera iz baze
    def delete(self):
        with Session(db_engine) as session:
            statement = select(DBUsers).where(DBUsers.id_email == self.email)
            user = session.exec(statement).first()
        if user:
            session.delete(user)
            session.commit()

    # Mijenja korisnikovu lozinku
    def update_password(self, password):
        with Session(db_engine) as session:
            statement = select(DBUsers).where(DBUsers.id_email == self.email)
            user = session.exec(statement).first()
        if user:
            user.password = password
            session.add(user)
            session.commit()

    @staticmethod
    def fetch(email):
        # Dohvaća user iz baze po email-u
        with Session(db_engine) as session:
            statement = select(DBUsers).where(DBUsers.id_email == email)
            user = session.exec(statement).first()
            if user:
                return Users(
                    email=user.id_email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    password=user.password,
                    is_admin=user.is_admin,
                )
            return None


class Admin(Users):
    def __init__(self, email, first_name, last_name, password):
        super().__init__(email, first_name, last_name, password, is_admin=True)

    def addEquipment(self, equipment_name, condition):
        with Session(db_engine) as session:
            statement = select(DBEquipment.id_equipment).order_by(
                DBEquipment.id_equipment.desc()
            )
            last_id = session.exec(statement).first()
            next_id = "EQ001" if last_id is None else f"EQ{int(last_id[2:]) + 1:03d}"

            db_equipment = DBEquipment(
                id_equipment=next_id,
                equipment_name=equipment_name,
                condition=condition,
                available=True,
            )
            session.add(db_equipment)
            session.commit()
            return db_equipment.id_equipment

    def editEquipment(self, id_equipment, equipment_name, condition, available):
        with Session(db_engine) as session:
            statement = select(DBEquipment).where(
                DBEquipment.id_equipment == id_equipment
            )
            equipment = session.exec(statement).first()
            if equipment:
                equipment.equipment_name = equipment_name
                equipment.condition = condition
                equipment.available = available
                session.commit()

    def deleteEquipment(self, id_equipment):
        with Session(db_engine) as session:
            statement = select(DBEquipment).where(
                DBEquipment.id_equipment == id_equipment
            )
            equipment = session.exec(statement).first()
            if equipment:
                session.delete(equipment)
                session.commit()

    def sendWarning(self):
        pass


class Equipment:
    def __init__(self, id_equipment, equipment_name, condition, available):
        self.id_equipment = id_equipment
        self.equipment_name = equipment_name
        self.condition = condition
        self.available = available

    def checkAvailability(self):
        return self.available

    @staticmethod
    def fetch(id_equipment):
        with Session(db_engine) as session:
            statement = select(DBEquipment).where(
                DBEquipment.id_equipment == id_equipment
            )
            equipment = session.exec(statement).first()
        if equipment:
            return Equipment(
                id_equipment=equipment.id_equipment,
                equipment_name=equipment.equipment_name,
                condition=equipment.condition,
                available=equipment.available,
            )
        return None
