## if you want to run this python script, make sure to change to a proper directory before running it.

import sqlite3;
##import os;
##path = os.path.dirname(os.path.abspath(__file__))
##db = sqlite3.connect(os.path.join(path, "database.db"))

db = sqlite3.connect("database.db")

if __name__ == "__main__":
    email = input("Enter email: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    password = input("Enter password: ")
    db.execute("INSERT INTO users (id_email, first_name, last_name, passwrd) VALUES (?, ?, ?, ?)", (email, first_name, last_name, password))
    db.commit()
    