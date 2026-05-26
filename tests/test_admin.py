import pytest
from database.py_classes import Admin, Users
from database.db_tables import db_engine, Equipment as DBEquipment
from sqlmodel import Session, select
from sqlalchemy import text


@pytest.fixture
def admin():

    admin = Admin("admin@gmail.com", "Admin", "User", "admin123")

    admin.add()

    yield admin


@pytest.fixture(autouse=True)
def clean_db():

    yield

    with Session(db_engine) as session:

        session.exec(text("DELETE FROM loan"))
        session.exec(text("DELETE FROM equipment"))
        session.exec(text("DELETE FROM users"))

        session.commit()


class TestAdmin:
    # unit test
    def test_admin_default_flag(self):

        admin = Admin("admin@gmail.com", "Admin", "User", "123")

        assert admin.is_admin is True

    # unit test
    def test_admin_inheritance(self):
        admin = Admin("a@gmail.com", "Ime", "Prezime", "123")
        assert isinstance(admin, Users)

    def test_add_equipment(self, admin):

        admin.addEquipment("projektor", "new")

        with Session(db_engine) as session:

            equipment = session.exec(
                select(DBEquipment).where(DBEquipment.equipment_name == "projektor")
            ).first()

            assert equipment is not None
            assert equipment.equipment_name == "projektor"
            assert equipment.condition == "new"
            assert equipment.available is True

    def test_edit_equipment_success(self, admin):

        admin.addEquipment("Projektor", "new")

        with Session(db_engine) as session:

            equipment = session.exec(
                select(DBEquipment).where(DBEquipment.equipment_name == "Projektor")
            ).first()

            equipment_id = equipment.id_equipment

        admin.editEquipment(equipment_id, "Zvučnik", "used", False)

        with Session(db_engine) as session:

            edited = session.exec(
                select(DBEquipment).where(DBEquipment.id_equipment == equipment_id)
            ).first()

        assert edited is not None
        assert edited.equipment_name == "Zvučnik"
        assert edited.condition == "used"
        assert edited.available is False

    def test_edit_non_existing_equipment(self, admin):

        result = admin.editEquipment("EQ999", "mikrofon", "new", True)

        assert result is None

    def test_delete_equipment_success(self, admin):

        admin.addEquipment("Projektor", "new")

        with Session(db_engine) as session:

            equipment = session.exec(
                select(DBEquipment).where(DBEquipment.equipment_name == "Projektor")
            ).first()

            equipment_id = equipment.id_equipment

        admin.deleteEquipment(equipment_id)

        with Session(db_engine) as session:

            deleted = session.exec(
                select(DBEquipment).where(DBEquipment.id_equipment == equipment_id)
            ).first()

        assert deleted is None
