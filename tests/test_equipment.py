import pytest
from database.py_classes import Equipment


def test_equipment_init():

    eq = Equipment(
        "EQ001",
        "Kosilica",
        "new",
        True
    )

    assert eq.id_equipment == "EQ001"

def test_checkAvailability():
    equipment = Equipment(1, "Kosilica", "new", True)
    assert equipment.checkAvailability() is True

def test_checkAvailability_false():
    equipment = Equipment(1, "Kosilica", "new", False)
    assert equipment.checkAvailability() is False

def test_equipment_condition():

    eq = Equipment(
        "EQ001",
        "Laptop",
        "used",
        True
    )

    assert eq.condition == "used"