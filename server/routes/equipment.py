from fastapi import APIRouter, HTTPException
from database.py_classes import Equipment


router = APIRouter(prefix="/equipment", tags=["Equipment"])


# GET ruta, pretraživanje prema id-u opreme
@router.get("/{id_equipment}")
def get_equipment(id_equipment: str):
    equipment = Equipment.fetch(id_equipment)
    if not equipment:
        raise HTTPException(status_code=404, detail="Oprema ne postoji")
    return equipment
