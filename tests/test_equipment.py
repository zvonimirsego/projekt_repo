import pytest

from database.py_classes import Equipment


# unit test
def test_equipment_init():

    eq = Equipment("EQ001", "Kosilica", "new", True)

    assert eq.id_equipment == "EQ001"


# unit test
def test_checkAvailability_true():
    equipment = Equipment(1, "Kosilica", "new", True)
    assert equipment.checkAvailability() is True


# unit test
def test_checkAvailability_false():
    equipment = Equipment(1, "Kosilica", "new", False)
    assert equipment.checkAvailability() is False


@pytest.mark.parametrize("condition", ["new", "used", "heavily used", "broken"])

# unit test
def test_equipment_conditions(condition):

    eq = Equipment("EQ001", "Laptop", condition, True)

    assert eq.condition == condition


def test_fetch_non_existing_equipment():
    eq = Equipment.fetch("ZZ999")

    assert eq is None
