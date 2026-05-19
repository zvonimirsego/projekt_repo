from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.py_classes import Admin

router = APIRouter(prefix="/admin_panel", tags=["Admin"])

admin = Admin("admin@mail.com", "Admin", "Admin", "sudo")

class EquipmentInstance(BaseModel):
    equipment_name: str
    condition: str
    available: bool

@router.post("/equipment")
def add_equipment(data: EquipmentInstance):
    id = admin.addEquipment(data.equipment_name, data.condition)
    return {"message": "Oprema uspješno dodana","id":id}

@router.put("/equipment/{id_equipment}")
def edit_equipment(id_equipment: str, data: EquipmentInstance):
    admin.editEquipment(id_equipment, data.equipment_name, data.condition, data.available)
    return {"message": "Oprema uspješno ažurirana"}

@router.delete("/equipment/{id_equipment}")
def delete_equipment(id_equipment: str):
    admin.deleteEquipment(id_equipment)
    return {"message": "Oprema uspješno obrisana"}