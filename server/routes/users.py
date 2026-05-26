from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.py_classes import Users
from datetime import date

router = APIRouter(prefix="/users", tags=["Users"])


# Opcenita Pydantic User instanca (FastAPI radi isključivo sa Pydantic BaseModel instancama)
class UserInstance(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str
    is_admin: bool = False


# Specijalna Pydantic user instanca za updejtanje lozinke
class UserUpdatePassword(BaseModel):
    password: str


# Specijalna Pydantic loan instanca za stvaranje rezervacije
class LoanCreate(BaseModel):
    id_equipment: str
    start_date: date


# GET ruta, dohvaćanje svih usera
@router.get("/all_users")
def all_users():
    users = Users.fetch_all()
    return users


# GET ruta, pretraživanje prema emailu korisnika
@router.get("/{email}")
def get_user(email: str):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")
    return {
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        # Maknuti, tu zbog testiranja PUT rute --
        "password": user.password,
        # --^
        "is_admin": user.is_admin,
    }


# POST ruta
@router.post("/")
def post_user(data: UserInstance):
    existing = Users.fetch(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Korisnik već postoji")
    user = Users(
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=data.password,
        is_admin=data.is_admin,
    )
    user.add()
    return {"message": "Korisnik uspješno kreiran"}


# DELETE ruta
@router.delete("/{email}")
def delete_user(email: str):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")
    user.delete()
    return {"message": "Korisnik uspješno obrisan"}


# PUT ruta
@router.put("/{email}")
def update_user(email: str, data: UserUpdatePassword):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")
    user.update_password(data.password)
    return {"message": "Lozinka uspješno ažurirana"}


@router.post("/{email}/loans")
def make_reservation(email: str, data: LoanCreate):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")

    try:
        user.makeReservation(data.id_equipment, data.start_date)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Rezervacija uspješno kreirana"}


@router.put("/{email}/return/{id_loan}")
def return_loan(email: str, id_loan: int):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")
    
    success = user.returnReservation(id_loan)
    if not success:
        raise HTTPException(status_code=400, detail="Posudba ne postoji ili je već vraćena")
    return {"message": "Posudba uspješno vraćena"}


@router.delete("/{email}/loans/{id_loan}")
def delete_reservation(email: str, id_loan: int):
    user = Users.fetch(email)
    if not user:
        raise HTTPException(status_code=404, detail="Korisnik ne postoji")
    result = user.deleteReservation(id_loan)
    if not result:
        raise HTTPException(status_code=404, detail="Rezervacija ne postoji")
    return {"message": "Rezervacija uspješno obrisana"}
