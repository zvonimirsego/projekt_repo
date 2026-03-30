import sqlite3
import os
import datetime
path = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.path.join(path, "database.db"))

loan_number = 1

def register_user():
    email = input("Enter email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = input("Enter password: ")
    db.execute("INSERT INTO users (id_email, first_name, last_name, passwrd) VALUES (?, ?, ?, ?)", (email, first_name, last_name, password))
    db.commit()

def register_equipment():
    id_equipment = input("Enter equipment ID: ")
    equipment_name = input("Enter equipment name: ")
    condition = input("Enter equipment condition: ")
    db.execute("INSERT INTO equipment (id_equipment, equipment_name, condition) VALUES (?, ?, ?)", (id_equipment, equipment_name, condition))
    db.commit()

def make_loan():
    email_user = input("Enter user email: ")
    id_equipment = input("Enter equipment ID: ")
    due_date = datetime.datetime.now().date() + datetime.timedelta(days=14)
    print(due_date)
    db.execute("INSERT INTO loan (id_loan, id_user, id_equipment, due_date) VALUES (?, ?, ?, ?)", (1, email_user, id_equipment, due_date))
    db.commit()
    ##loan_number += 1

def db_reset():
    pass

if __name__ == "__main__":
    register_user()
    register_equipment()
    make_loan()
    
    print(db.execute("SELECT * FROM loan WHERE id_user = ?", ("zsego",)).fetchall())