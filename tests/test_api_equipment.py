import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from sqlalchemy import text

from server.main import app
from database.py_classes import Admin
from database.db_tables import db_engine

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    yield
    with Session(db_engine) as session:
        session.exec(text("DELETE FROM equipment"))
        session.commit()


@pytest.fixture
def seeded_equipment():
    admin = Admin("setup@test.com", "Setup", "Setup", "x")
    eq_id = admin.addEquipment("Bušilica", "new")
    yield eq_id


def test_get_equipment_success(seeded_equipment):
    response = client.get(f"/equipment/{seeded_equipment}")

    assert response.status_code == 200
    body = response.json()
    assert body["id_equipment"] == seeded_equipment
    assert body["equipment_name"] == "Bušilica"
    assert body["condition"] == "new"
    assert body["available"] is True


def test_get_equipment_not_found():
    response = client.get("/equipment/NONEXISTENT")

    assert response.status_code == 404
    assert response.json()["detail"] == "Oprema ne postoji"
