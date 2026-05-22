import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from sqlalchemy import text
from datetime import date, timedelta

from server.main import app
from database.py_classes import Users, Admin
from database.db_tables import db_engine, Loan as DBLoan

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    yield
    with Session(db_engine) as session:
        session.exec(text("DELETE FROM loan"))
        session.exec(text("DELETE FROM equipment"))
        session.exec(text("DELETE FROM users"))
        session.commit()


@pytest.fixture
def user_and_equipment():
    Users("loaner@test.com", "Loan", "Tester", "pw").add()
    admin = Admin("setup@test.com", "Setup", "Setup", "x")
    eq_id = admin.addEquipment("Bušilica", "new")
    yield "loaner@test.com", eq_id


def _loan_body(eq_id, days=7):
    return {
        "id_equipment": eq_id,
        "start_date": date.today().isoformat(),
        "due_date": (date.today() + timedelta(days=days)).isoformat(),
    }


def test_make_reservation_success(user_and_equipment):
    email, eq_id = user_and_equipment

    response = client.post(f"/users/{email}/loans", json=_loan_body(eq_id))

    assert response.status_code == 200
    assert response.json()["message"] == "Rezervacija uspješno kreirana"


def test_make_reservation_user_not_found(user_and_equipment):
    _, eq_id = user_and_equipment

    response = client.post("/users/nobody@test.com/loans", json=_loan_body(eq_id))

    assert response.status_code == 404
    assert response.json()["detail"] == "Korisnik ne postoji"


def test_make_reservation_equipment_not_found(user_and_equipment):
    email, _ = user_and_equipment

    response = client.post(f"/users/{email}/loans", json=_loan_body("FAKE123"))

    assert response.status_code == 400
    assert response.json()["detail"] == "Oprema ne postoji"


def test_make_reservation_equipment_unavailable(user_and_equipment):
    email, eq_id = user_and_equipment
    body = _loan_body(eq_id)

    # Prva rezervacija uspjesna -> postavlja equipment.available na False
    first = client.post(f"/users/{email}/loans", json=body)
    assert first.status_code == 200


    # Druga rezervacija (bi trebala biti) neuspješna jer je oprema već rezervirana 
    second = client.post(f"/users/{email}/loans", json=body)
    assert second.status_code == 400
    assert second.json()["detail"] == "Oprema nije dostupna"


def test_delete_reservation_success(user_and_equipment):
    email, eq_id = user_and_equipment

    create = client.post(f"/users/{email}/loans", json=_loan_body(eq_id))
    assert create.status_code == 200

    # Ruta ne vraća id rezervacije -> moramo ga dohvatiti iz baze
    with Session(db_engine) as session:
        loan = session.exec(select(DBLoan).where(DBLoan.id_user == email)).first()
        loan_id = loan.id_loan

    response = client.delete(f"/users/{email}/loans/{loan_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Rezervacija uspješno obrisana"