from .db_tables import db_engine, Users as DBUsers, Loan as DBLoan, Equipment as DBEquipment, db_reset
from sqlmodel import Session, select
from datetime import date, timedelta

class Loan:
    brojac = -1
    with Session(db_engine) as session:
        statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan.desc())
        last_id = session.exec(statement).first()
        brojac = 1 if last_id is None else last_id + 1
    
    def __init__(self, id_user, id_equipment, starting_date, due_date, returned=False, id_loan=None):
        self.id_loan = id_loan if id_loan is not None else Loan.brojac
        self.id_user = id_user
        self.id_equipment = id_equipment
        self.starting_date = starting_date
        self.due_date = due_date
        self.returned = returned
        with Session(db_engine) as session:
            statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan.desc())
            last_id = session.exec(statement).first()
            Loan.brojac = Loan.brojac + 1 if last_id is None else last_id + 1
    
    @staticmethod
    def fetch(id_loan):
        with Session(db_engine) as session:
            statement = select(DBLoan).where(DBLoan.id_loan == id_loan)
            loan = session.exec(statement).first()
            if loan:
                return Loan(
                    id_loan=loan.id_loan,
                    id_user=loan.id_user,
                    id_equipment=loan.id_equipment,
                    starting_date=loan.start_date,
                    due_date=loan.due_date,
                    returned=loan.returned
                )
            return None
    
    @staticmethod
    def fetch_all():
        with Session(db_engine) as session:
            statement = select(DBLoan)
            loan_list = session.exec(statement).all()
            return [Loan(
                id_loan=loan.id_loan,
                id_user=loan.id_user,
                id_equipment=loan.id_equipment,
                starting_date=loan.start_date,
                due_date=loan.due_date,
                returned=loan.returned
            ) for loan in loan_list]

class Users:
    def __init__(self, email, first_name, last_name, password, is_admin=False):
        #za is_admin vidjeti file na desktopu
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin


    def makeReservation(self, id_equipment, starting_date, due_date):
        with Session(db_engine) as session:
            statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan.desc())
            last_id = session.exec(statement).first()
            next_id = 1 if last_id is None else last_id + 1

            #ako cemo staviti da id_loan bude prvi slobodan
            #   statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan)
            #   loan_ids = session.exec(statement).all()
            #   next_id = 1
            #   for existing_id in loan_ids:
            #       if existing_id == next_id:
            #           next_id += 1
            #       else:
            #           break
            
            equipment = session.exec(
                select(DBEquipment).where(DBEquipment.id_equipment == id_equipment)
            ).first()
            if not equipment:
                raise ValueError("Oprema ne postoji")
            if not equipment.available:
                raise ValueError("Oprema nije dostupna")
            equipment.available = False

            db_loan = DBLoan(
                id_loan=next_id,
                id_user=self.email,
                id_equipment=id_equipment,
                start_date=starting_date,
                due_date=due_date,
                returned=False
            )
            session.add(db_loan)
            session.commit()

            return True

    def deleteReservation(self, id_loan):
        loan_local = Loan.fetch(id_loan)
        if loan_local and loan_local.id_user == self.email and loan_local.starting_date < date.today():
            with Session(db_engine) as session:
                statement = select(DBLoan).where(DBLoan.id_loan == id_loan, DBLoan.id_user == self.email)
                loan = session.exec(statement).first()
                if loan:
                    session.delete(loan)
                    session.commit()
                    return True
                return False

    #dodati naredbu za fetch i za addanje u bazu

    def add(self):
        with Session(db_engine) as session:
            db_user = DBUsers(
                id_email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_admin=self.is_admin
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
        #Dohvaća user iz baze po email-u
        with Session(db_engine) as session:
            statement = select(DBUsers).where(DBUsers.id_email == email)
            user = session.exec(statement).first()
            if user:
                return Users(
                    email=user.id_email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    password=user.password,
                    is_admin=user.is_admin
                )
            return None
    
    @staticmethod
    def fetch_all():
        #Dohvaća sve usere iz baze
        with Session(db_engine) as session:
            statement = select(DBUsers)
            user_list = session.exec(statement).all()
            return [Users(
                email=user.id_email,
                first_name=user.first_name,
                last_name=user.last_name,
                password=user.password,
                is_admin=user.is_admin
            ) for user in user_list]

class Admin(Users):
    def __init__(self, email, first_name, last_name, password):
        super().__init__(email, first_name, last_name, password, is_admin=True)

    def addEquipment(self, equipment_name, condition):
        equipment_local = Equipment(id_equipment=None, equipment_name=equipment_name, condition=condition, available=True)
        
        with Session(db_engine) as session:
            statement = select(DBEquipment.id_equipment).order_by(DBEquipment.id_equipment.desc())
            last_id = session.exec(statement).first()
            next_id = "EQ001" if last_id is None else f"EQ{int(last_id[2:]) + 1:03d}"
            equipment_local.id_equipment = next_id

            db_equipment = DBEquipment(
                id_equipment=equipment_local.id_equipment,
                equipment_name=equipment_local.equipment_name,
                condition=equipment_local.condition,
                available=equipment_local.available
            )
            session.add(db_equipment)
            session.commit()
            return db_equipment.id_equipment

    def editEquipment(self, id_equipment, equipment_name, condition, available):
        equipment_local = Equipment(id_equipment=id_equipment, equipment_name=equipment_name, condition=condition, available=available)
        with Session(db_engine) as session:
            statement = select(DBEquipment).where(DBEquipment.id_equipment == equipment_local.id_equipment)
            equipment_db = session.exec(statement).first()
            if equipment_db:
                equipment_db.equipment_name = equipment_local.equipment_name
                equipment_db.condition = equipment_local.condition
                equipment_db.available = equipment_local.available
                session.commit()

    def deleteEquipment(self, id_equipment):
        with Session(db_engine) as session:
            statement = select(DBEquipment).where(DBEquipment.id_equipment == id_equipment)
            equipment_db = session.exec(statement).first()
            if equipment_db:
                session.delete(equipment_db)
                session.commit()

    def sendWarning(self, id_loan):
        loan = Loan.fetch(id_loan)
        if loan and not loan.returned and loan.due_date < date.today():
            # Ovdje bi se implementirala logika slanja upozorenja korisniku, npr. emailom
            print(f"Warning sent to {loan.id_user} for loan {loan.id_loan}")
    

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
            statement = select(DBEquipment).where(DBEquipment.id_equipment == id_equipment)
            equipment = session.exec(statement).first()
            if equipment:
                return Equipment(
                    id_equipment=equipment.id_equipment,
                    equipment_name=equipment.equipment_name,
                    condition=equipment.condition,
                    available=equipment.available
                )
            return None