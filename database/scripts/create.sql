DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS equipment;
DROP TABLE IF EXISTS loan;

CREATE TABLE IF NOT EXISTS users(
    id_email VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    passwrd VARCHAR(50) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS equipment(
    id_equipment VARCHAR(10) PRIMARY KEY,
    equipment_name VARCHAR(100) NOT NULL,
    condition VARCHAR(20) CHECK (condition in ('new', 'used', 'heavily used', 'broken')),
    available BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS loan(
    id_loan INTEGER PRIMARY KEY,
    id_user VARCHAR(50) REFERENCES users(id_email),
    id_equipment VARCHAR(10) REFERENCES equipment(id_equipment),
    starting_date DATE DEFAULT CURRENT_DATE,
    due_date DATE
);