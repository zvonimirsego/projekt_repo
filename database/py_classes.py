from db_tables import db_engine, Users as DBUsers, Loan as DBLoan, Equipment as DBEquipment, db_reset
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
        Loan.brojac += 1
    
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


    def makeReservation(self, id_equipment, starting_date=date.today(), due_date=date.today() + timedelta(days=14)):
        loan = Loan(self.email, id_equipment, starting_date, due_date, False)
        # ovo je lokalna verzija posudbe, "klikom" na potvrdu cemo pushati na bazu. Tu bi se "uredjivale stvari na stranici".
        
        with Session(db_engine) as session:
            # Mozda dodje korisno kasnije
            # statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan.desc())
            # last_id = session.exec(statement).first()
            # next_id = 1 if last_id is None else last_id + 1

            #ako cemo staviti da id_loan bude prvi slobodan
            #   statement = select(DBLoan.id_loan).order_by(DBLoan.id_loan)
            #   loan_ids = session.exec(statement).all()
            #   next_id = 1
            #   for existing_id in loan_ids:
            #       if existing_id == next_id:
            #           next_id += 1
            #       else:
            #           break

            db_loan = DBLoan(
                id_loan=loan.id_loan,
                id_user=loan.id_user,
                id_equipment=loan.id_equipment,
                start_date=loan.starting_date,
                due_date=loan.due_date,
                returned=loan.returned
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
        #Dodaje usera u bazu
        with Session(db_engine) as session:
            db_user = DBUsers(
                id_email=self.email,
                first_name=self.first_name,
                last_name=self.last_name,
                password=self.password,
                is_admin=self.is_admin
            )
            session.add(db_user)
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
    
    def add(self):
        with Session(db_engine) as session:
            db_equipment = DBEquipment(
                id_equipment=self.id_equipment,
                equipment_name=self.equipment_name,
                condition=self.condition,
                available=self.available
            )
            session.add(db_equipment)
            session.commit()
    
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
    
    @staticmethod
    def fetch_all():
        with Session(db_engine) as session:
            statement = select(DBEquipment)
            equipment_list = session.exec(statement).all()
            return [Equipment(
                id_equipment=equipment.id_equipment,
                equipment_name=equipment.equipment_name,
                condition=equipment.condition,
                available=equipment.available
            ) for equipment in equipment_list]

if __name__ == "__main__":
    db_reset()
    user = Users(email="zsego@university.hr", first_name="Zvonimir", last_name="Šego", password="password123")
    equipment = Equipment(id_equipment="EQ001", equipment_name="Busilica", condition="new", available=True)
    user.add()
    equipment.add()
    user.makeReservation(id_equipment="EQ001")
    equipment2 = Equipment(id_equipment="EQ002", equipment_name="Čekić", condition="used", available=True)
    equipment2.add()
    user.makeReservation(id_equipment="EQ002")
    loans = Loan.fetch_all()
    for loan in loans:
        print(f"Loan ID: {loan.id_loan}, User: {loan.id_user}, Equipment: {loan.id_equipment}, Start: {loan.starting_date}, Due: {loan.due_date}, Returned: {loan.returned}")