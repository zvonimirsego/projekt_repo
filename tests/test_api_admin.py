import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from sqlalchemy import text

from server.main import app
from database.db_tables import db_engine, Equipment as DBEquipment

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_db():
    yield
    with Session(db_engine) as session:
        session.exec(text("DELETE FROM equipment"))
        session.commit()


def _create_equipment_via_api(name="Projektor", condition="new", available=True):
    response = client.post(
        "/admin_panel/equipment",
        json={"equipment_name": name, "condition": condition, "available": available},
    )
    assert response.status_code == 200, f"setup POST failed: {response.text}"
    return response.json()["id"]


def test_add_equipment():
    response = client.post(
        "/admin_panel/equipment",
        json={"equipment_name": "Projektor", "condition": "new", "available": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["message"] == "Oprema uspješno dodana"
    assert "id" in body

   
   # provjeravamo da je oprema dodana u bazu s ispravnim poljima
    with Session(db_engine) as session:
        stmt = select(DBEquipment).where(DBEquipment.id_equipment == body["id"])
        equipment = session.exec(stmt).first()
        assert equipment is not None
        assert equipment.equipment_name == "Projektor"


def test_edit_equipment():
    eq_id = _create_equipment_via_api(name="Zvučnik", condition="new")

    response = client.put(
        f"/admin_panel/equipment/{eq_id}",
        json={"equipment_name": "Mikrofon", "condition": "used", "available": False},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Oprema uspješno ažurirana"


    # ponovno dohvatimo opremu GET-om i provjerimo jesu li se polja promijenila
    fetched = client.get(f"/equipment/{eq_id}").json()
    assert fetched["equipment_name"] == "Mikrofon"
    assert fetched["condition"] == "used"
    assert fetched["available"] is False


def test_delete_equipment():
    eq_id = _create_equipment_via_api(name="Kosilica")

    response = client.delete(f"/admin_panel/equipment/{eq_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "Oprema uspješno obrisana"

    # GET -> trebalo bi vratiti 404
    fetched = client.get(f"/equipment/{eq_id}")
    assert fetched.status_code == 404