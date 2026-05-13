import os
from datetime import date, timedelta
from sqlmodel import create_engine, SQLModel, Field
#from sqlmodel import Session, select

path = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(path, "database.db")
reset_script_path = os.path.join(path, "scripts", "create.sql")

db_engine = create_engine(f"sqlite:///{db_path}")

class Users(SQLModel, table=True):
    id_email: str = Field(primary_key=True)
    first_name: str
    last_name: str
    password: str
    is_admin: bool | None = False

class Equipment(SQLModel, table=True):
    id_equipment: str = Field(primary_key=True)
    equipment_name: str
    condition: str
    available: bool | None = True

class Loan(SQLModel, table=True):
    id_loan: int = Field(primary_key=True)
    id_user: str = Field(foreign_key="users.id_email")
    id_equipment: str = Field(foreign_key="equipment.id_equipment")
    start_date: date | None = Field(default_factory=date.today)
    due_date: date | None = Field(default_factory=lambda: date.today() + timedelta(days=14))
    returned: bool | None = False

if __name__ == "__main__":
    with open(reset_script_path, "r", encoding="utf-8") as file:
        sql_script = file.read()

    with db_engine.raw_connection() as connection:
        connection.executescript(sql_script)
        connection.commit()
    
    # zsego = Users(id_email="zsego@university.hr", first_name="Zvonimir", last_name="Šego", password="password123")
    # busilica = Equipment(id_equipment="EQ001", equipment_name="Busilica", condition="new")
    # loan1 = Loan(id_loan=1, id_user="zsego@university.hr", id_equipment="EQ001")
    
    # with Session(db_engine) as session:
    #     session.add(zsego)
    #     session.add(busilica)
    #     session.add(loan1)
    #     session.commit()
    
    # with Session(db_engine) as session:
    #     statement = select(Users)
    #     user = session.exec(statement).first()
    #     print(user)
    
    # with Session(db_engine) as session:
    #     statement = select(Equipment)
    #     equipment = session.exec(statement).first()
    #     print(equipment)
    
    # with Session(db_engine) as session:
    #    statement = select(Loan)
    #    loan = session.exec(statement).first()
    #    print(loan)

    print("DB reset")