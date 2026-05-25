from fastapi import APIRouter, HTTPException
from database.py_classes import Equipment

router = APIRouter(prefix="/equipment", tags=["Equipment"])


# GET ruta, dohvaćanje sve opreme
@router.get("/all_equipment")
def all_equipment():
    equipment = Equipment.fetch_all()
    return equipment


# GET ruta, dohvaćanje sve dostupne opreme
@router.get("/all_available")
def all_available():
    available = Equipment.fetch_available()
    return available


# GET ruta, pretraživanje prema id-u opreme
@router.get("/{id_equipment}")
def get_equipment(id_equipment: str):
    equipment = Equipment.fetch(id_equipment)
    if not equipment:
        raise HTTPException(status_code=404, detail="Oprema ne postoji")
    return equipment
