import pytest
from classes import Equipment


def test_checkAvailability():
    equipment = Equipment(1, "Kosilica", "new", True)
    assert equipment.checkAvailability() is True

def test_checkAvailability_false():
    equipment = Equipment(1, "Kosilica", "new", False)
    assert equipment.checkAvailability() is False